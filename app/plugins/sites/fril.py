import re
import requests
from urllib.parse import urlparse
from urllib.parse import urlencode
from bs4 import BeautifulSoup

#
name = "Fril"

#
def get(driver, keyword):
	query = { "query": keyword, "sort": "created_at", "order": "desc", "transaction": "selling" }
	#quoted_keyword = quote_plus(keyword)
	return requests.get(f"https://fril.jp/s?{urlencode(query)}").text

# イテレータ
def extract(documents):
	bs = BeautifulSoup(documents, "html.parser")
	if not bs.select_one(".nohit"):
		for item in bs.select(".item"):
			url = item.select_one("a")["href"]
			id = re.search("fril.jp/([0-9a-z]+)", url).group(1)
			title = item.select_one(".item-box__item-name").get_text(strip=True)
			img_url = urlparse(item.select_one("meta")["content"])
			img = img_url.scheme + "://" + img_url.netloc + img_url.path
			price_str = item.select_one(".item-box__item-price").get_text(strip=True)
			price = int("".join([c for c in price_str if c in [str(i) for i in range(10)]]))
			yield (id, url, title, img, price)
