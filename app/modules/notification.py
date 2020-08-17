import datetime
from smtplib import SMTP_SSL
from email.utils import formatdate
from email.mime.text import MIMEText
from modules.config import mail_from, mail_to, mail_bcc, smtp_host, smtp_port, smtp_user, smtp_passwd

# メッセージオブジェクトをつくる関数
def create_message(frm, to, bcc, subject, body):
	msg = MIMEText(body)
	msg["Subject"] = subject
	msg["From"] = frm
	msg["To"] = to
	msg["Bcc"] = bcc
	msg["Date"] = formatdate()
	return msg

# SMTPサーバーを通してメールを送る関数
def smtp_send(host, port, user, password, mailfrom, mailto, messages):
	if len(messages) == 0:
		return
	with SMTP_SSL(host, port) as smtp:
		smtp.login(user, password)
		for message in messages:
			smtpobj.sendmail(mailfrom, mailto, message.as_string())

# 複数のメールを設定に基づいて送信する
def send(mails):
	messages = [create_message(mail_from, mail_to, mail_bcc, subject, body) for subject, body in mails]
	smtp_send(smtp_host, smtp_port, smtp_user, smtp_passwd, mail_from, mail_to, messages)

# 通知配信を制限に則って行うクラス
class NotificationController():

	# コンストラクタ
	def __init__(self, max_per_hour):
		self.count = 0
		self.hour = datetime.datetime.now().strftime("%Y-%m-%d %H")
		self.max_per_hour = max_per_hour

	# 複数のメールを設定に基づいて時間あたりの最大件数を超えないように送信する
	def send(self, mails):
		hour = datetime.datetime.now().strftime("%Y-%m-%d %H")
		if self.hour != hour:
			self.hour = hour
			self.count = 0
		num = min(len(mails), self.max_per_hour - self.count)
		self.count += num
		send(mails[0:num])
		return num
