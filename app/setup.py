import os
from shutil import rmtree
from modules.logging import log_dir
from modules.database import data_dir, db_path, connect
from modules.utilities import mkdirp

# データのクリーンアップ
rmtree(log_dir, ignore_errors=True)
rmtree(data_dir, ignore_errors=True)

# 各種ディレクトリをつくる
mkdirp(log_dir)
mkdirp(data_dir)

# データベース作成
with connect() as connection:
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS keyword(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, keyword TEXT NOT NULL UNIQUE, importance REAL NOT NULL)")
	cursor.execute("CREATE TABLE IF NOT EXISTS filter(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, pattern TEXT NOT NULL UNIQUE)")
	cursor.execute("CREATE TABLE IF NOT EXISTS history(site TEXT NOT NULL, keyword INTEGER NOT NULL, UNIQUE(site, keyword))")
	cursor.execute("CREATE TABLE IF NOT EXISTS item(site TEXT NOT NULL, url TEXT NOT NULL UNIQUE, title TEXT NOT NULL, img TEXT NOT NULL, price INTEGER NOT NULL, added TIMESTAMP DEFAULT (DATETIME('now', 'localtime')))")

# データベースをPHPから操作できるようにパーミッションを変える
os.chmod(data_dir, 0o777)
os.chmod(db_path, 0o777)
