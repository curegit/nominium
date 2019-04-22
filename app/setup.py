import os
import sqlite3

# カレントディレクトリ変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ログディレクトリをつくる
logdir = "logs"
if not os.path.exists(logdir):
	os.mkdir(logdir)

# DB作成
dbname = "ziraffem.db"
connection = sqlite3.connect(dbname, isolation_level=None)
cursor = connection.cursor()
sql = "CREATE TABLE IF NOT EXISTS item(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL UNIQUE, name TEXT, img_url TEXT, added TIMESTAMP DEFAULT (DATETIME('now', 'localtime')))"
cursor.execute(sql)
sql = "CREATE TABLE IF NOT EXISTS keyword(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, keyword TEXT NOT NULL UNIQUE, importance REAL NOT NULL, count INTEGER NOT NULL DEFAULT 0)"
cursor.execute(sql)
connection.close()

# PHPから操作できるようにディレクトリとDBのパーミッションを変える
os.chmod(".", 0o777)
os.chmod(dbname, 0o777)
