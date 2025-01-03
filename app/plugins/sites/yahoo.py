import re
from urllib.parse import urlparse, quote, urlencode
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# サイトの識別子
name = "Yahoo"

# フェッチャーにさせる動作
def get(driver, keyword):
	path = quote(keyword, safe="")
	query = urlencode({"sort": "openTime", "order": "desc", "open": "1"})
	driver.get(f"https://paypayfleamarket.yahoo.co.jp/search/{path}?{query}")
	container = driver.find_element(By.TAG_NAME, "body")
	return container.get_attribute("innerHTML")

# フェッチしたデータの処理
def extract(documents):
	bs = BeautifulSoup(documents, "html.parser")
	if itm := bs.select_one("#itm"):
		for item in itm.select("a"):
			url = "https://paypayfleamarket.yahoo.co.jp" + item["href"]
			match = re.search("/item/([A-Za-z0-9]+)", url)
			id = match.group(1)
			title = item.select_one("img")["alt"]
			thumbnail = item.select_one("img")["src"]
			img_url = urlparse(thumbnail)
			img = img_url.scheme + "://" + img_url.netloc + img_url.path
			price_str = item.select_one("p").get_text(strip=True)
			price = int("".join([c for c in price_str if c in [str(i) for i in range(10)]]))
			yield id, url, title, img, thumbnail, price
