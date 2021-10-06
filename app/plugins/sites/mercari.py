import re
from urllib.parse import urlparse
from urllib.parse import urlencode
from bs4 import BeautifulSoup

# サイトの識別子
name = "Mercari"

# フェッチャーにさせる動作
def get(driver, keyword):
	query = { "keyword": keyword, "sort": "created_time", "order": "desc", "status": "on_sale" }
	driver.get(f"https://jp.mercari.com/search?{urlencode(query)}")
	container = driver.find_element_by_id("search-result")
	return container.get_attribute("innerHTML")

# フェッチしたデータの処理
def extract(documents):
	bs = BeautifulSoup(documents, "html.parser")
	if not bs.select_one(".empty-state"):
		for b in bs.select("li"):
			path = urlparse(b.select_one("a")["href"]).path
			id = re.search("/(m[0-9]+)/", path).group(1)
			url = "https://jp.mercari.com" + path
			title = b.select_one(".item-name").get_text(strip=True)
			img_url = urlparse(b.select_one("img")["src"])
			img = img_url.scheme + "://" + img_url.netloc + img_url.path
			price_str = b.select_one(".number").get_text(strip=True)
			price = int("".join([c for c in price_str if c in [str(i) for i in range(10)]]))
			yield (id, url, title, img, price)
