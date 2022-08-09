from re import search
from time import time, sleep
from threading import Thread
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from modules.config import driver_path, headless

# WebDriverを起動する
def init_driver():
	options = Options()
	if headless:
		options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-gpu")
	options.add_argument("--incognito")
	options.add_argument("--window-size=1920,1080")
	options.add_argument("--disable-extensions")
	options.add_argument("--disable-desktop-notifications")
	options.add_argument("--blink-settings=imagesEnabled=false")
	options.add_argument("--ignore-certificate-errors")
	options.add_argument("--allow-running-insecure-content")
	options.add_argument("--disable-web-security")
	options.add_argument("--lang=ja")
	return Chrome(executable_path=driver_path, options=options)

# フェッチャースレッド
class Fetcher(Thread):

	# コンストラクタ
	def __init__(self, id, driver, logger, in_queue, out_queue, wait=1, max_rate=5):
		super().__init__(daemon=True)
		self.id = id
		self.driver = driver
		self.logger = logger
		self.in_queue = in_queue
		self.out_queue = out_queue
		self.wait = wait
		self.max_rate = max_rate
		self.complete = False

	# フェッチャースレッドの動作
	def run(self):
		self.logger.log_line(f"フェッチャー {self.id} が起動しました。")
		while True:
			if self.complete:
				break
			start = time()
			maybe_task = self.in_queue.get()
			if maybe_task is None:
				break
			site, kid, keyword = maybe_task
			self.logger.log_line(f"フェッチャー {self.id} が {site.name} で「{keyword}」をロードします。")
			try:
				documents = site.get(self.driver, keyword)
			except Exception as e:
				self.logger.log_exception(e, f"フェッチャー {self.id} が {site.name} でフェッチに失敗しました。")
			else:
				self.logger.log_line(f"フェッチャー {self.id} がフェッチを完了しました。")
				self.out_queue.put((site, kid, keyword, documents))
			sleep(self.wait)
			elapsed = time() - start
			if elapsed < self.max_rate:
				sleep(self.max_rate - elapsed)
		self.logger.log_line(f"フェッチャー {self.id} が終了しました。")

# 必要な情報の抽出器
class Extractor():

	# コンストラクタ
	def __init__(self, logger, queue, max_price, cut=10, enough=100):
		self.logger = logger
		self.queue = queue
		self.max_price = max_price
		self.cut = cut
		self.enough = enough
		self.cache = set()
		self.history = set()
		self.fresh = set()
		self.filter_patterns = []

	# 新規のフェッチをすべて取り出す
	def pop_fresh(self):
		fresh = list(self.fresh)
		self.fresh = set()
		return fresh

	# キューにある情報をすべて抽出
	def pop_all_items(self, least_one=False, timeout=None):
		qsize = max(1, self.queue.qsize()) if least_one else self.queue.qsize()
		for i in range(qsize):
			try:
				site, kid, keyword, documents = self.queue.get(timeout=timeout)
			except:
				break
			else:
				fresh = (site.name, kid) not in self.history
			try:
				count = 0
				cut_count = 0
				put_count = 0
				for item in site.extract(documents):
					count += 1
					id, url, title, img, price = item
					assert type(id) == type(url) == type(title) == type(img) == str
					assert type(price) == int
					id_pair = (site.name, id)
					if id_pair in self.cache:
						cut_count += 1
					else:
						cut_count = 0
						self.cache.add(id_pair)
						notify = not fresh
						if price > self.max_price:
							notify = False
						if notify:
							for pattern in self.filter_patterns:
								if search(pattern, title) is not None:
									notify = False
						put_count += 1
						yield (site, keyword, notify, item)
					if count >= self.enough:
						break
					if cut_count >= self.cut:
						break
				if fresh:
					self.fresh.add((site.name, kid))
					self.history.add((site.name, kid))
			except Exception as e:
				self.logger.log_exception(e, f"{site.name} からの「{keyword}」についての抽出に失敗しました（{put_count} 件送出済み）。")
			else:
				if put_count > 0:
					self.logger.log_line(f"{site.name} から「{keyword}」について {count} 件抽出した内 {put_count} 件を送出しました。")
