import os
import configparser
from selenium import webdriver

#
def load_appconf():

def load_settings():





# カレントディレクトリ変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Chromeドライバーへのパス
config = configparser.SafeConfigParser()
config.read("settings.ini")
driver_path = config.get("general", "driver")

# 読み込むURL
url = "http://example.com/"

# オプションをつくる
options = webdriver.ChromeOptions() 
options.add_argument("--headless")

# バグ回避
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

# いらない機能
options.add_argument("--disable-desktop-notifications")
options.add_argument("--disable-extensions")

# 画像を読まない
options.add_argument("--blink-settings=imagesEnabled=false")

# エラーの許容
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-web-security")

# スタート
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

# ページ取得
driver.get(url)

# ソース出力
print(driver.page_source)

# 終了
driver.quit()
