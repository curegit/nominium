#!/usr/bin/env python3

import sys
import os
from shutil import rmtree
from modules.logging import log_dir, create_log_dir
from modules.database import data_dir, db_path, connect
from modules.crawling import wdm_dir
from modules.utilities import mkdirp, confirm_cui

# 誤実行防止
if not confirm_cui("初期化シーケンスを実行しますか？"):
	sys.exit(1)

# データのクリーンアップ
rmtree(log_dir, ignore_errors=True)
rmtree(data_dir, ignore_errors=True)
rmtree(wdm_dir, ignore_errors=True)

# 各種ディレクトリをつくる
create_log_dir()
mkdirp(data_dir)

# データベース作成
with connect() as connection:
	cursor = connection.cursor()
	cursor.execute("DROP TABLE IF EXISTS keyword")
	cursor.execute("DROP TABLE IF EXISTS filter")
	cursor.execute("DROP TABLE IF EXISTS history")
	cursor.execute("DROP TABLE IF EXISTS item")
	cursor.execute("CREATE TABLE IF NOT EXISTS keyword(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, keyword TEXT NOT NULL UNIQUE, importance REAL NOT NULL, priority INTEGER NOT NULL DEFAULT 0, send INTEGER NOT NULL DEFAULT 1, hook INTEGER NOT NULL DEFAULT 1, CHECK(importance > 0.0 AND importance <= 1.0), CHECK(send IN (0, 1)), CHECK(hook IN (0, 1)))")
	cursor.execute("CREATE TABLE IF NOT EXISTS filter(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, pattern TEXT NOT NULL UNIQUE)")
	cursor.execute("CREATE TABLE IF NOT EXISTS history(site TEXT NOT NULL, keyword INTEGER NOT NULL, UNIQUE(site, keyword))")
	cursor.execute("CREATE TABLE IF NOT EXISTS item(site TEXT NOT NULL, id TEXT NOT NULL, url TEXT NOT NULL UNIQUE, title TEXT NOT NULL, img TEXT NOT NULL, thumbnail TEXT NOT NULL, price INTEGER NOT NULL, notify INTEGER NOT NULL, added TIMESTAMP DEFAULT (DATETIME('now', 'localtime')), UNIQUE(site, id))")
	cursor.execute("VACUUM")

# データベースをPHPから操作できるようにパーミッションを変える
os.chmod(data_dir, 0o777)
os.chmod(db_path, 0o666)
