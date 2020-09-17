import re
from urllib.parse import urlparse
from urllib.parse import urlencode
from bs4 import BeautifulSoup

# サイトの識別子
name = "Mercari"

# フェッチャーにさせる動作
def get(driver, keyword):
	query = { "keyword": keyword, "sort_order": "created_desc", "status_on_sale": "1" }
	driver.get(f"https://www.mercari.com/jp/search/?{urlencode(query)}")
	container = driver.find_element_by_class_name("items-box-container")
	return container.get_attribute("outerHTML")

# フェッチしたデータの処理
def extract(documents):
	bs = BeautifulSoup(documents, "html.parser")
	if not bs.select_one(".search-result-description"):
		for b in bs.select(".items-box"):
			path = urlparse(b.select_one("a")["href"]).path
			id = re.search("/(m[0-9]+)/", path).group(1)
			url = "https://www.mercari.com" + path
			title = b.select_one("h3").get_text(strip=True)
			img_url = urlparse(b.select_one("img")["data-src"])
			img = img_url.scheme + "://" + img_url.netloc + img_url.path
			price_str = b.select_one(".items-box-price").get_text(strip=True)
			price = int("".join([c for c in price_str if c in [str(i) for i in range(10)]]))
			yield (id, url, title, img, price)
