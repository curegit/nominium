import json
import datetime
import psutil
from modules.database import data_dir
from modules.utilities import file_path

# サイトごとのクエリを保存する関数
def save_queries(sites):
	queries = {}
	for site in sites:
		if site.name in queries:
			raise RuntimeError(f"サイト「{site.name}」が重複しています")
		try:
			queries[site.name] = site.queryjs
		except Exception:
			pass
	with open(file_path(data_dir, "queries", "json"), "wb") as f:
		f.write(json.dumps(queries).encode("utf-8"))

# プロセス情報を保存する関数
def save_process_info(length):
	# 自身のPIDを取得
	pid = psutil.Process().pid
	start_time = int(psutil.Process().create_time())
	data = {"pid": pid, "start_time": start_time, "end_time": int(length) + start_time}
	with open(file_path(data_dir, "process", "json"), "wb") as f:
		f.write(json.dumps(data).encode("utf-8"))
