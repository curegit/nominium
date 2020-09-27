from shutil import rmtree
from modules.logging import log_dir
from modules.database import connect
from modules.utilities import mkdirp

# ログをすべて消す
rmtree(log_dir, ignore_errors=True)
mkdirp(log_dir)

# データベースの蓄積データを消す
with connect() as connection:
	cursor = connection.cursor()
	cursor.execute("DELETE FROM history")
	cursor.execute("DELETE FROM item")
	cursor.execute("VACUUM")
