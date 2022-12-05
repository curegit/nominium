#!/usr/bin/env python3

from sys import stderr
from time import sleep
from modules.config import mail_enabled
from modules.crawling import init_driver
from modules.notification import send

# WebDriverのテスト
print("WebDriver をテストします")
try:
	driver = init_driver()
except:
	print("ブラウザの起動に失敗しました", file=stderr)
	print("WebDriver の設定または環境に問題があります", file=stderr)
	print("テストを中断します")
	raise
try:
	driver.get("https://example.com/")
	sleep(5)
except:
	print("example.com の取得に失敗しました", file=stderr)
	print("WebDriver の設定または環境に問題があります", file=stderr)
	print("テストを中断します")
	raise
else:
	print("example.com の取得に成功しました")
	print("WebDriver のエラーは観測されませんでした")
finally:
	driver.quit()

# メール送信のテスト
if mail_enabled:
	print("SMTP 構成をテストします")
	try:
		send([("テストメール", "Nominium テストメールです。", "<html><head><title>テストメール</title></head><body><p>Nominium テストメールです。</p></body></html>")])
	except:
		print("メールを送信できませんでした", file=stderr)
		print("SMTP の構成または環境に問題があります", file=stderr)
		print("テストを中断します")
		raise
	else:
		print("メールを送信しました")
else:
	print("メール通知が無効なので SMTP テストを実施しません")

print("テストは完了しました")
