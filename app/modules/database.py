import sqlite3
from modules.utilities import file_path, rel_path

# データベースファイルへのパス
data_dir = rel_path("../../data")
db_path = file_path(data_dir, "nominium", "db")

# データベースに接続する
def connect():
	connection = sqlite3.connect(db_path, isolation_level=None)
	connection.row_factory = sqlite3.Row
	return connection
