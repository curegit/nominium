import configparser
from util import file_relpath

# アプリケーション構成を読み込む
def read_appconf():
	config = configparser.SafeConfigParser()
	config.read(file_relpath("../../conf/app.ini"))
	return {sec: {opt: config.get(sec, opt) for opt in config.options(sec)} for sec in config.sections()}

# ユーザ設定を読み込む
def read_settings():
	config = configparser.SafeConfigParser()
	config.read(file_relpath("../../conf/settings.ini"))
	return {sec: {opt: config.get(sec, opt) for opt in config.options(sec)} for sec in config.sections()}
