import os
import os.path
import inspect

# ディレクトリ、ディレクトリ内部からのファイルパス、拡張子からパスを構築する
def filepath(dirpath, filepath, ext):
	path = os.path.join(dirpath, filepath) + os.extsep + ext
	return os.path.normpath(path)

# 特定ファイルからの相対パスを構築する（デフォルトは呼び出し元のスクリプトからの相対パス）
def file_relpath(relpath, file=None):
	filename = file if file is not None else inspect.stack()[1].filename
	directory = os.getcwd() if filename == "<stdin>" else os.path.dirname(filename)
	return os.path.join(directory, relpath)
