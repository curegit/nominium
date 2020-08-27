from modules.crawling import init_driver
from modules.notification import send

# WebDriverのテスト
driver = init_driver()
driver.get("http://example.com/")
driver.quit()

# メール送信のテスト
send([("テストメール", "Nominium テストメールです。")])
