import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# サイトの識別子
name = "Mercari"

# フェッチャーにさせる動作
def get(driver, keyword):
	query = {"keyword": keyword, "sort": "created_time", "order": "desc", "status": "on_sale"}
	driver.get(f"https://jp.mercari.com/search?{urlencode(query)}")
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search-result a, #search-result mer-empty-state")))
	container = driver.find_element(By.ID, "search-result")
	return container.get_attribute("innerHTML")

# フェッチしたデータの処理
def extract(documents):
	bs = BeautifulSoup(documents, "html.parser")
	for b in bs.select("li"):
		path = b.select_one("a")["href"]
		id = re.search("/(m[0-9]+)", path).group(1)
		url = "https://jp.mercari.com/item/" + id
		thum = b.select_one("mer-item-thumbnail")
		title = thum["item-name"]
		img = "https://static.mercdn.net/item/detail/orig/photos/" + id + "_1.jpg"
		thumbnail = "https://static.mercdn.net/c!/w=240/thumb/photos/" + id + "_1.jpg"
		price = int(thum["price"])
		yield id, url, title, img, thumbnail, price
