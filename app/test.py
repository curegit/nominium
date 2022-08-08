from modules.crawling import init_driver
from modules.notification import send

# WebDriverのテスト
driver = init_driver()
driver.get("https://example.com/")
driver.quit()

# メール送信のテスト
if mail_enabled:
	send([("テストメール", "Nominium テストメールです。", "<html><head><title>テストメール</title></head><body><p>Nominium テストメールです。</p></body></html>")])
