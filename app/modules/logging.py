import datetime
from queue import Queue
from modules.utilities import file_path, rel_path

# ログを保存するディレクトリ
log_dir = rel_path("../../logs")

# 日付に応じてログファイルのパスを返す
def log_file_path(dtime):
	log_name = dtime.strftime("%Y-%m-%d")
	return file_path(log_dir, log_name, "log")

# ログに書く時刻情報の文字列を返す
def time_string(dtime):
	return dtime.strftime("[%Y-%m-%d %H:%M:%S]")

# ログの行フォーマットを施した文字列を返す
def log_line_format(dtime, message):
	return f"{time_string(dtime)} {message}\n"

# 複数スレッドから集約的に書き込むためのロガー
class Logger():

	# コンストラクタ
	def __init__(self):
		self.queue = Queue()

	# ログキューに1行追記する
	def log_line(self, message):
		self.queue.put((datetime.datetime.now(), message))

	# ログキューに発生した例外情報を追記する
	def log_exception(self, exception, message=None):
		if message is None:
			self.log_line(str(exception))
		else:
			self.log_line(f"{message}\n{(str(exception)).rstrip()}")

	# キューにあるログをファイルに書き込む（非スレッドセーフ）
	def commit(self):
		qsize = self.queue.qsize()
		if qsize > 0:
			dtime, message = self.queue.get()
			log_path = log_file_path(dtime)
			pending = qsize
			while pending > 0:
				with open(log_path, mode="a", encoding="utf-8") as file:
					file.write(log_line_format(dtime, message))
					pending -= 1
					while pending > 0:
						dtime, message = self.queue.get()
						if log_file_path(dtime) != log_path:
							log_path = log_file_path(dtime)
							break
						file.write(log_line_format(dtime, message))
						pending -= 1
