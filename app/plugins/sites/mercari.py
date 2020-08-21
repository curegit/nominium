import re
from urllib.parse import urlparse
from urllib.parse import urlencode
from bs4 import BeautifulSoup

#
name = "Mercari"

#
def get(driver, keyword):
	query = { "keyword": keyword, "sort_order": "created_desc", "status_on_sale": "1" }
	driver.get(f"https://www.mercari.com/jp/search/?{urlencode(query)}")
	if len(driver.find_elements_by_class_name("search-result-description")) > 0:
		return []
	items = driver.find_elements_by_class_name("items-box")
	return [i.get_attribute("outerHTML") for i in items]

# イテレータ
def extract(documents):
	for document in documents:
		bs = BeautifulSoup(document, "html.parser")
		path = urlparse(bs.select_one("a")["href"]).path
		id = re.search("/m([0-9]+)/", path).group(1)
		url = "https://www.mercari.com" + path
		title = bs.select_one("h3").get_text(strip=True)
		img_url = urlparse(bs.select_one("img")["data-src"])
		img = img_url.scheme + "://" + img_url.netloc + img_url.path
		price = int("".join([d for d in bs.select_one(".items-box-price").get_text(strip=True) if d != "¥" and d != ","]))
		yield (id, url, title, img, price)
