import re
from urllib.parse import urlparse
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# サイトの識別子
name = "Mercari"

# フェッチャーにさせる動作
def get(driver, keyword):
	query = { "keyword": keyword, "sort": "created_time", "order": "desc", "status": "on_sale" }
	driver.get(f"https://jp.mercari.com/search?{urlencode(query)}")
	container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search-result")))
	return container.get_attribute("innerHTML")

# フェッチしたデータの処理
def extract(documents):
	bs = BeautifulSoup(documents, "html.parser")
	for b in bs.select("li"):
		path = b.select_one("a")["href"]
		id = re.search("/(m[0-9]+)", path).group(1)
		url = "https://jp.mercari.com" + path
		thum = b.select_one("mer-item-thumbnail")
		title = thum["item-name"]
		img_url = urlparse(thum["src"])
		img = img_url.scheme + "://" + img_url.netloc + img_url.path
		price = int(thum["price"])
		yield (id, url, title, img, price)
