import sys
import time
import random
from queue import Queue
from modules import config as conf
from modules.logging import Logger
from modules.database import connect
from modules.crawling import init_driver, Fetcher, Extractor
from modules.notification import NotificationController
from plugins.enabled import sites

# 目標動作時間を受け取る
uptime = int(sys.argv[1])

# 開始時刻を記録する
start = time.time()

# タスクキューを作成する
fetch_queue = Queue(conf.parallel * 2)
documents_queue = Queue()

# ロギングを開始する
logger = Logger()
logger.log_line("プロセスを開始しました。")
logger.commit()

# フェッチャーを起動する
drivers = []
try:
	for i in range(conf.parallel):
		drivers.append(init_driver())
except Exception as e:
	try:
		logger.log_exception(e, "フェッチャーの起動に失敗しました。")
		logger.commit()
	except:
		pass
	for driver in drivers:
		try:
			driver.quit()
		except:
			pass
	raise
fetchers = [Fetcher(i, d, logger, fetch_queue, documents_queue, conf.wait, conf.max_rate) for i, d in enumerate(drivers, 1)]
for fetcher in fetchers:
	fetcher.start()

# フェッチタスクのイテレータを用意する
fetch_table = []
def fetch_iterater():
	while True:
		count = 0
		for kid, keyword, probability in fetch_table:
			if random.random() < probability:
				for site in sites:
					count += 1
					yield site, kid, keyword
		if count == 0:
			yield None
fetch_iter = fetch_iterater()

# データベースに繋いで作業する
with connect() as connection:
	cursor = connection.cursor()
	# ここでのエラーはログに残るがプログラムも終了する
	try:
		# 存在しないサイトのフェッチ履歴を削除する
		holders = ", ".join(["?"] * len(sites))
		site_names = tuple([site.name for site in sites])
		cursor.execute(f"DELETE FROM history WHERE site NOT IN ({holders})", site_names)
		# 抽出器を用意して必要なら履歴を引き継ぐ
		extractor = Extractor(logger, documents_queue, conf.max_price, conf.cut, conf.enough)
		if conf.while_stopped:
			cursor.execute("SELECT * FROM history")
			for hr in cursor.fetchall():
				extractor.history.add((hr["site"], int(hr["keyword"])))
		# 通知コントローラを用意する
		nc = NotificationController(conf.max_notify_hourly)
		# 動作時間内なら続ける
		while time.time() - start < uptime:
			# キーワードを取り出してイテレータを更新する
			cursor.execute("SELECT * FROM keyword")
			fetch_table = [(int(kr["id"]), kr["keyword"], float(kr["importance"])) for kr in cursor.fetchall()]
			# フェッチタスクをキューに入るだけ入れる
			for i in range(fetch_queue.maxsize - fetch_queue.qsize()):
				maybe_fetch = next(fetch_iter)
				if maybe_fetch is None:
					break
				fetch_queue.put(maybe_fetch)
			# フィルタを更新する
			cursor.execute("SELECT * FROM filter")
			extractor.filter_patterns = [fr["pattern"] for fr in cursor.fetchall()]
			#
			mails = []
			for site, keyword, notify, item in extractor.pop_all_items():
				id, url, title, img, price = item
				cursor.execute("SELECT COUNT(*) AS count FROM item WHERE site = ? AND id = ?", (site.name, id))
				existence = bool(int(cursor.fetchone()["count"]))
				if not existence:
					cursor.execute("INSERT INTO item(site, id, url, title, img, price) VALUES(?, ?, ?, ?, ?, ?)", (site.name, id, url, title, img, price))
					if notify:
						subject = f"{site.name}: {title}"
						body = f"{title}\n{price}\n{url}\n\n{img}\n"
						mails.append((subject, body))
						logger.log_line(f"通知 {subject}")
			# 履歴を更新する
			for site, kid in extractor.pop_fresh():
				cursor.execute("SELECT COUNT(*) AS count FROM history WHERE site = ? AND keyword = ?", (site, kid))
				existence = bool(int(cursor.fetchone()["count"]))
				if not existence:
					cursor.execute("INSERT INTO history(site, keyword) VALUES(?, ?)", (site, kid))
			# 通知
			if mails:
				try:
					count = nc.send(mails)
					logger.log_line(f"通知を {count} 送信しました。")
				except Exception as e:
					logger.log_exception(e, f"メールの送信に失敗しました。")
			# ログに書き込む
			logger.commit()
	#
	except Exception as e:
		try:
			logger.log_exception(e, "重大なエラーが発生")
			logger.commit()
		except:
			pass
		raise
	# リソース開放などの後始末を行う
	finally:
		# フェッチャーを終了させる
		for fetcher in fetchers:
			fetcher.complete = True
		for fetcher in fetchers:
			if fetch_queue.full:
				break
			fetch_queue.put(None, block=False)
		for fetcher in fetchers:
			fetcher.join(timeout=60)
		# ブラウザを終了させる
		for driver in drivers:
			try:
				driver.quit()
			except Exception as e:
				logger.log_exception(e, "ブラウザの終了に失敗しました。")
			else:
				logger.log_line("ブラウザを正常に終了させました。")

#
logger.log_line("プロセスを終了しました。")
logger.commit()
