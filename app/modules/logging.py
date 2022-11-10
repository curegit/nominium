import sys
import datetime
import traceback
from queue import Queue
from threading import Lock
from modules.utilities import file_path, rel_path

# ログを保存するディレクトリ
log_dir = rel_path("../../logs")

# 日付に応じてログファイルのパスを返す
def log_file_path(dtime, error=False):
	log_name = dtime.strftime("%Y-%m-error" if error else "%Y-%m-%d")
	return file_path(log_dir, log_name, "log")

# ログに書く時刻情報の文字列を返す
def time_string(dtime):
	return dtime.strftime("[%Y-%m-%d %H:%M:%S]")

# ログの行フォーマットを施した文字列を返す
def log_line_format(dtime, message, eol=True):
	return f"{time_string(dtime)} {message}" + ("\n" if eol else "")

# 複数スレッドから集約的に書き込むためのロガー
class Logger():

	# 標準出力への排他書き込み用プリミティブ
	lock = Lock()

	# コンストラクタ
	def __init__(self, tee=True):
		self.queue = Queue()
		self.err_queue = Queue()
		self.tee = tee

	# ログキューに1行追記する
	def log_line(self, message, stderr=False):
		dtime = datetime.datetime.now()
		if self.tee:
			with Logger.lock:
				print(log_line_format(dtime, message, eol=False), file=(sys.stderr if stderr else sys.stdout), flush=True)
		self.queue.put((dtime, message))
		if stderr:
			self.err_queue.put((dtime, message))

	# ログキューに発生した例外情報を追記する
	def log_exception(self, exception, message=None):
		trace = "".join(traceback.TracebackException.from_exception(exception).format())
		message = message or (str(exception)).rstrip()
		self.log_line(f"{message}\n{trace.rstrip()}", stderr=True)

	# キューにあるログをファイルに書き込む（非スレッドセーフ）
	def commit(self):
		for queue, error in [(self.queue, False), (self.err_queue, True)]:
			qsize = queue.qsize()
			if qsize > 0:
				pending = qsize
				dtime, message = queue.get()
				log_path = log_file_path(dtime, error=error)
				while pending > 0:
					with open(log_path, mode="a", encoding="utf-8") as file:
						file.write(log_line_format(dtime, message))
						pending -= 1
						while pending > 0:
							dtime, message = queue.get()
							if log_file_path(dtime) != log_path:
								log_path = log_file_path(dtime)
								break
							file.write(log_line_format(dtime, message))
							pending -= 1
