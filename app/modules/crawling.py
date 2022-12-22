from re import compile, IGNORECASE
from time import time, sleep
from threading import Thread
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from modules.config import browser, use_wdm, driver_path, headless
from modules.logging import log_dir
from modules.utilities import file_path, rel_path

# WDMのキャッシュ保存先
wdm_dir = rel_path("../../app/caches")

# ブラウザのウィンドウサイズ
width = 1280
height = 1024

# WebDriverを起動する
def init_driver():
	if browser == "firefox":
		driver = init_gecko_driver()
	elif browser == "chrome":
		driver = init_chrome_driver(chromium=False)
	elif browser == "chromium":
		driver = init_chrome_driver(chromium=True)
	else:
		raise ValueError(f"ブラウザ {browser} は不正です")
	return setup_driver(driver)

# ブラウザ共通の初期設定処理
def setup_driver(driver):
	driver.get("http://example.com/")
	driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
	return driver

# Firefoxを起動する
def init_gecko_driver():
	log_path = file_path(log_dir, "geckodriver", "log")
	if use_wdm:
		from webdriver_manager.firefox import GeckoDriverManager
		service = FirefoxService(GeckoDriverManager(path=wdm_dir).install(), log_path=log_path)
	else:
		service = FirefoxService(executable_path=driver_path, log_path=log_path)
	options = FirefoxOptions()
	if headless:
		options.add_argument("-headless")
	options.add_argument("-safe-mode")
	options.add_argument("-private")
	options.add_argument(f"-width={width}")
	options.add_argument(f"-height={height}")
	options.set_preference("permissions.default.image", 2)
	options.set_preference("permissions.default.desktop-notification", 2)
	options.set_preference("dom.webnotifications.enabled", False)
	options.set_preference("browser.cache.disk.enable", False)
	options.set_preference("browser.cache.memory.enable", False)
	options.set_preference("browser.cache.offline.enable", False)
	options.set_preference("network.http.use-cache", False)
	return Firefox(service=service, options=options)

# Chromeを起動する
def init_chrome_driver(chromium=False):
	log_path = file_path(log_dir, "chromedrive", "log")
	if use_wdm:
		from webdriver_manager.chrome import ChromeDriverManager
		from webdriver_manager.core.utils import ChromeType
		if chromium:
			service = ChromeService(ChromeDriverManager(path=wdm_dir, chrome_type=ChromeType.CHROMIUM).install(), log_path=log_path)
		else:
			service = ChromeService(ChromeDriverManager(path=wdm_dir).install(), log_path=log_path)
	else:
		service = ChromeService(executable_path=driver_path, log_path=log_path)
	options = ChromeOptions()
	if headless:
		options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-gpu")
	options.add_argument("--incognito")
	options.add_argument("--disk-cache-size=0")
	options.add_argument(f"--window-size={width},{height}")
	options.add_argument("--disable-blink-features=AutomationControlled")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--disable-extensions")
	options.add_argument("--disable-desktop-notifications")
	options.add_argument("--blink-settings=imagesEnabled=false")
	options.add_argument("--ignore-certificate-errors")
	options.add_argument("--allow-running-insecure-content")
	options.add_argument("--disable-web-security")
	options.add_argument("--lang=ja")
	# 一部環境用
	# options.add_argument("--remote-debugging-port=9222")
	return Chrome(service=service, options=options)

# フェッチャースレッド
class Fetcher(Thread):

	# コンストラクタ
	def __init__(self, id, driver, logger, in_queue, out_queue, wait=1, max_rate=5, patience=3, backoff=3600):
		super().__init__(daemon=True)
		self.id = id
		self.driver = driver
		self.logger = logger
		self.in_queue = in_queue
		self.out_queue = out_queue
		self.wait = wait
		self.max_rate = max_rate
		self.patience = patience
		self.backoff = backoff
		self.complete = False
		self.failures = dict()
		self.logger.log_line(f"フェッチャー {self.id} が起動しました。")

	# フェッチャースレッドの動作
	def run(self):
		self.logger.log_line(f"フェッチャー {self.id} が開始しました。")
		while True:
			if self.complete:
				break
			start = time()
			maybe_task = self.in_queue.get()
			if maybe_task is None:
				break
			site, kid, keyword = maybe_task
			if self.should_backoff(site, kid):
				self.logger.log_line(f"フェッチャー {self.id} は {site.name} での「{keyword}」のロードをスキップします。")
				continue
			self.logger.log_line(f"フェッチャー {self.id} が {site.name} で「{keyword}」をロードします。")
			try:
				documents = site.get(self.driver, keyword)
			except Exception as e:
				self.logger.log_exception(e, f"フェッチャー {self.id} が {site.name} でフェッチに失敗しました。")
				self.record_failure(site, kid)
			else:
				self.logger.log_line(f"フェッチャー {self.id} がフェッチを完了しました。")
				self.out_queue.put((site, kid, keyword, documents))
				self.mark_as_successful(site, kid)
			sleep(self.wait)
			elapsed = time() - start
			if elapsed < self.max_rate:
				sleep(self.max_rate - elapsed)
		self.logger.log_line(f"フェッチャー {self.id} が終了しました。")

	# フェッチ失敗記録を消す
	def mark_as_successful(self, site, kid):
		self.failures.pop((site.name, kid), None)

	# フェッチ失敗を記録
	def record_failure(self, site, kid):
		if (site.name, kid) in self.failures:
			n, t = self.failures[(site.name, kid)]
			if time() - t < self.backoff:
				self.failures[(site.name, kid)] = n + 1, time()
			else:
				self.failures[(site.name, kid)] = 1, time()
		else:
			self.failures[(site.name, kid)] = 1, time()

	# 様子見するか判断する
	def should_backoff(self, site, kid):
		if (site.name, kid) in self.failures:
			n, t = self.failures[(site.name, kid)]
			if n >= self.patience and time() - t < self.backoff:
				return True
		return False

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
		self.filter_regexs = []

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
					id, url, title, img, thumbnail, price = item
					assert type(id) == type(url) == type(title) == type(img) == type(thumbnail) == str
					assert type(price) == int
					id_pair = (site.name, id)
					if id_pair in self.cache:
						cut_count += 1
					else:
						cut_count = 0
						self.cache.add(id_pair)
						notify = not fresh
						notify_code = 0 if notify else 1
						if price > self.max_price:
							notify = False
							notify_code = 2
						if notify:
							for regex in self.filter_regexs:
								if regex.search(title) is not None:
									notify = False
									notify_code = 3
						put_count += 1
						yield site, keyword, notify, notify_code, item
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

	# フィルタの正規表現パターンを設定する
	def set_filter_patterns(self, patterns):
		self.filter_regexs = []
		for pattern in patterns:
			try:
				self.filter_regexs.append(compile(pattern, flags=IGNORECASE))
			except Exception as e:
				self.logger.log_exception(e, f"パターン「{pattern}」は正規表現として不正です。")
