import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# サイトの識別子
name = "Fril"

# フェッチャーにさせる動作
def get(driver, keyword):
	query = {"query": keyword, "sort": "created_at", "order": "desc", "transaction": "selling"}
	response = requests.get("https://fril.jp/s", params=query, timeout=20)
	# Frilは検索結果が空のときに404が返る実装になっている
	if response.status_code != 404:
		response.raise_for_status()
	return response.text

# フェッチしたデータの処理
def extract(documents):
	bs = BeautifulSoup(documents, "html.parser")
	if not bs.select_one(".nohit"):
		for item in bs.select(".item"):
			url = item.select_one("a")["href"]
			id = re.search("fril.jp/([0-9a-z]+)", url).group(1)
			title = item.select_one(".item-box__item-name").get_text(strip=True)
			img_url = urlparse(item.select_one("img")["data-original"])
			thumbnail = img_url.scheme + "://" + img_url.netloc + img_url.path
			img = thumbnail.replace("/m/", "/l/")
			price_str = item.select_one(".item-box__item-price").get_text(strip=True)
			price = int("".join([c for c in price_str if c in [str(i) for i in range(10)]]))
			yield id, url, title, img, thumbnail, price
