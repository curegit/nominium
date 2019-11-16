import os
import sqlite3
import random
import time
import datetime
import configparser
import urllib.parse
from time import sleep
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

# カレントディレクトリ変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Chromeドライバーへのパス
config = configparser.SafeConfigParser()
config.read("settings.ini")
driver_path = config.get("general", "driver")

# メール関係の設定
email = config.get("general", "email")
bcc = config.get("general", "bcc")
smtp = config.get("general", "smtp")
port = int(config.get("general", "port"))
efrom = config.get("general", "from")
user = config.get("general", "user")
password = config.get("general", "password")

# 目標稼働時間
target_time = int(config.get("general", "time"))

# 発火確率
possibility = float(config.get("general", "possibility"))

# 最大処理数
max_items = int(config.get("general", "max_items"))

# ログを1行追記する関数
def write_log_line(str):
	filename = "./logs/" + datetime.date.today().strftime("%Y-%m-%d") + ".log"
	with open(filename, mode="a") as file:
		file.write(str + "\n")

# 現在時刻をフォーマットして返す関数
def my_time():
	return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

# メール文字列をつくる関数
def create_message(efrom, to, bcc, subject, body):
	msg = MIMEText(body)
	msg["Subject"] = subject
	msg["From"] = efrom
	msg["To"] = to
	msg["Bcc"] = bcc
	msg["Date"] = formatdate()
	return msg

# SMTPサーバーを通してメールを送る関数
def send(smtp, port, user, password, efrom, to, msg):
	smtpobj = smtplib.SMTP_SSL(smtp, port)
	smtpobj.login(user, password)
	smtpobj.sendmail(efrom, to, msg.as_string())
	smtpobj.quit()

# メールを送る関数
def sendmail(subject, body):
	msg = create_message(efrom, email, bcc, subject, body)
	send(smtp, port, user, password, efrom, email, msg)

# 開始時刻を保存
start = time.time()

# 開始を記録
write_log_line(my_time() + " Started")

# ランダムウェイト
sleep(random.randrange(200))

# ここのエラーはログに残るがプログラムも終了する
try:

	# DB接続
	dbname = "ziraffem.db"
	connection = sqlite3.connect(dbname, isolation_level=None)
	connection.row_factory = sqlite3.Row
	cursor = connection.cursor()

	# ブラウザ起動
	options = webdriver.ChromeOptions()
	options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument("--lang=ja")
	options.add_argument("--disable-gpu")
	options.add_argument("--disable-desktop-notifications")
	options.add_argument("--disable-extensions")
	options.add_argument("--blink-settings=imagesEnabled=false")
	options.add_argument("--ignore-certificate-errors")
	options.add_argument("--allow-running-insecure-content")
	options.add_argument("--disable-web-security")
	driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

	# 稼働時間内なら続ける
	while target_time > time.time() - start:

		# ランダムウェイト
		sleep(random.randrange(10) + 5)

		# キーワード取得
		sql = "SELECT * FROM keyword"
		cursor.execute(sql)
		keyword_records = cursor.fetchall()

		# キーワードごとに処理
		for kr in keyword_records:

			# 確率的にやったりやらなかったりする
			if random.random() < possibility * float(kr["importance"]):

				# 初回の巡回は通知しない
				inform = False
				sql = "SELECT SUM(count) AS count FROM keyword WHERE id = ?"
				cursor.execute(sql, (kr["id"],))
				sum = int(cursor.fetchone()["count"])
				if sum > 0:
					inform = True

				# すべてのクロールが成功したらTrue
				result = True

				# ログに記録
				write_log_line(my_time() + " Crawling: " + kr["keyword"])

				# メルカリについて処理する
				try:

					# ページ遷移
					url = "https://www.mercari.com/jp/search/?status_on_sale=1&sort_order=created_desc&page=1&keyword={}".format(kr["keyword"])
					driver.get(url)
					write_log_line(my_time() + " Loaded: Mercari")

					# 検索結果があるか確認
					hit = driver.find_elements_by_class_name("search-result-description")
					if not len(hit) == 0:
						write_log_line(my_time() + " No hits: {}".format(kr["keyword"]))
					else:

						# 商品のRemote WebDriver WebElementを抜き出す
						items = driver.find_elements_by_class_name("items-box")
						write_log_line(my_time() + " {} hit(s): {}".format(len(items), kr["keyword"]))

						# それぞれの属性を抜き出す
						for k, i in enumerate(items):
							name = i.find_element_by_class_name("items-box-name").text
							url = i.find_element_by_tag_name("a").get_attribute("href")
							p = urllib.parse.urlparse(url)
							url = p.scheme + "://" + p.netloc + p.path
							img_url = i.find_element_by_tag_name("img").get_attribute("data-src")
							price = i.find_element_by_class_name("items-box-price").text

							# すでに存在するものか確認
							sql = "SELECT COUNT(*) AS count FROM item WHERE url = ?"
							cursor.execute(sql, (url,))
							r = int(cursor.fetchone()["count"])
							if r == 0:

								# メール送信
								if inform and k <= max_items:
									subject = "Mercari: {}".format(name)
									body = "{}\n{}\n{}\n\n{}\n".format(name, price, url, img_url)
									sendmail(subject, body)
									write_log_line(my_time() + " Sent: `{}`".format(subject))

								# DB登録
								sql = "INSERT INTO item(url, name, img_url) VALUES(?, ?, ?)"
								cursor.execute(sql, (url, name, img_url))

				# エラーをログに書いて続行
				except Exception as e:
					result = False
					write_log_line(my_time() + " " + str(e))

				finally:
					write_log_line(my_time() + " Done: Mercari")

				# ラクマについて処理する
				try:

					# ページ遷移
					url = "https://fril.jp/search/{}/page/1?order=desc&sort=item_id&transaction=selling".format(kr["keyword"])
					driver.get(url)
					write_log_line(my_time() + " Loaded: Rakuma")

					# 検索結果があるか確認
					hit = driver.find_elements_by_class_name("nohit")
					if not len(hit) == 0:
						write_log_line(my_time() + " No hits: {}".format(kr["keyword"]))
					else:

						# 商品のRemote WebDriver WebElementを抜き出す
						items = driver.find_elements_by_class_name("item")
						write_log_line(my_time() + " {} hit(s): {}".format(len(items), kr["keyword"]))

						# それぞれの属性を抜き出す
						for k, i in enumerate(items):
							name = i.find_element_by_class_name("item-box__item-name").text
							url = i.find_element_by_tag_name("a").get_attribute("href")
							img_url = i.find_element_by_tag_name("img").get_attribute("data-original")
							p = urllib.parse.urlparse(img_url)
							img_url = p.scheme + "://" + p.netloc + p.path
							price = i.find_element_by_class_name("item-box__item-price").text

							# すでに存在するものか確認
							sql = "SELECT COUNT(*) AS count FROM item WHERE url = ?"
							cursor.execute(sql, (url,))
							r = int(cursor.fetchone()["count"])
							if r == 0:

								# メール送信
								if inform and k <= max_items:
									subject = "Rakuma: {}".format(name)
									body = "{}\n{}\n{}\n\n{}\n".format(name, price, url, img_url)
									sendmail(subject, body)
									write_log_line(my_time() + " Sent: `{}`".format(subject))

								# DB登録
								sql = "INSERT INTO item(url, name, img_url) VALUES(?, ?, ?)"
								cursor.execute(sql, (url, name, img_url))

				# エラーをログに書いて続行
				except Exception as e:
					result = False
					write_log_line(my_time() + " " + str(e))

				finally:
					write_log_line(my_time() + " Done: Rakuma")

				# すべて成功したら巡回カウントアップ
				if result:
					sql = "UPDATE keyword SET count = count + 1 WHERE id = ?"
					cursor.execute(sql, (kr["id"],))

# ログに書く
except Exception as e:
	write_log_line(my_time() + " " + str(e))

# 後始末
finally:

	# DB切断
	try:
		connection.close()
	except:
		pass

	# ブラウザ終了
	try:
		driver.quit()
	except:
		pass

# 終了を記録
write_log_line(my_time() + " Stopped")
