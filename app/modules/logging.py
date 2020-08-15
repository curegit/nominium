import datetime
from modules.utilities import file_path, rel_path

# ログに書く時刻情報の文字列を返す
def time_string():
	return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

# 現在の日付に応じてログファイルのパスを返す
def log_file_path():
	log_dir = rel_path("../../logs")
	log_name = datetime.date.today().strftime("%Y-%m-%d")
	return file_path(log_dir, log_name, "log")

# 今日のログに1行追記する
def log_line(str):
	with open(log_file_path(), mode="a", encoding="utf-8") as file:
		file.write(f"{time_string()} {str}\n")

# ログに発生した例外情報を追記する
def log_exception(exception):
	log_line(str(exception))

# 今日のログに1行追記する（失敗しても例外を送出しない）
def try_log_line(str):
	try:
		log_line(str)
	except:
		pass

# ログに発生した例外情報を追記する（失敗しても例外を送出しない）
def try_log_line(exception):
	try:
		log_exception(exception)
	except:
		pass
