import datetime

# 現在時刻をフォーマットして返す関数
def my_time():
	return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

# ログを一行追記する関数
def write_log_line(logdir):
	filename = "./logs/" + datetime.date.today().strftime("%Y-%m-%d") + ".log"
	with open(filename, mode="a") as file:
		file.write(str + "\n")
