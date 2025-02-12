import re
from urllib.parse import urlparse, quote, urlencode
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# サイトの識別子
name = "Yahoo"

# 検索URLを生成する関数 (JavaScript)
queryjs = """
	((keyword) => {
		const path = encodeURIComponent(keyword);
		const params = new URLSearchParams({
			keyword: keyword,
			sort: "openTime",
			order: "desc",
			open: "1"
		});
		return "https://paypayfleamarket.yahoo.co.jp/search/" + path + "?" + params.toString();
	})
"""

# 検索URLを生成する関数
def query(keyword):
	path = quote(keyword, safe="")
	query = urlencode({"sort": "openTime", "order": "desc", "open": "1"})
	return f"https://paypayfleamarket.yahoo.co.jp/search/{path}?{query}"

# フェッチャーにさせる動作
def get(driver, keyword):
	driver.get(query(keyword))
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
			price_digits = "".join([c for c in price_str if c in [str(i) for i in range(10)]])
			try:
				price = int(price_digits)
			except ValueError:
				if len(price_digits) <= 3:
					price = 0
				else:
					raise
			yield id, url, title, img, thumbnail, price
