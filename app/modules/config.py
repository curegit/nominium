import configparser
from modules.utilities import file_path, rel_path

# 設定を保存するファイルへのパス
conf_dir = rel_path("../../conf")
conf_path = file_path(conf_dir, "settings", "ini")

# 設定値をすべて読み込む
config = configparser.ConfigParser()
config.read(conf_path)

# 全般的な設定
wait = int(config.get("general", "wait"))
max_rate = int(config.get("general", "max_rate"))
cut = int(config.get("general", "cut"))
enough = int(config.get("general", "enough"))
n_fetchers = int(config.get("general", "n_fetchers"))
n_extracters = int(config.get("general", "n_extracters"))
max_notify_hourly = int(config.get("general", "max_notify_hourly"))
while_stopped = bool(int(config.get("general", "while_stopped")))

# Seleniumの設定
driver_path = config.get("selenium", "driver")

# SMTP関係の設定
mail_to = config.get("smtp", "to")
mail_from = config.get("smtp", "from")
mail_bcc = config.get("smtp", "bcc")
smtp_host = config.get("smtp", "host")
smtp_port = int(config.get("smtp", "port"))
smtp_user = config.get("smtp", "user")
smtp_passwd = config.get("smtp", "password")