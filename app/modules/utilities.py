import os
import os.path
import inspect

# 足りないディレクトリを再帰的に作成する
def mkdirp(path):
	os.makedirs(path, exist_ok=True)

# ディレクトリ、ファイル名、拡張子を結合し正規化して返す
def file_path(dirpath, filename, ext):
	path = f"{os.path.join(dirpath, filename)}.{ext}"
	return os.path.normpath(path)

# 呼び出し元スクリプトを起点とする相対パスを絶対化して返す
def rel_path(relpath):
	filename = inspect.stack()[1].filename
	dirpath = os.path.dirname(filename)
	return os.path.join(dirpath, relpath)

# コンソールで確認を求める
def confirm_cui(message):
	while True:
		r = input(f"{message} [y/n]").strip().lower()
		if r == "y":
			return True
		elif r == "n":
			return False
