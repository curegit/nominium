import datetime
from smtplib import SMTP_SSL
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from modules.config import mail_from, mail_to, smtp_host, smtp_port, smtp_user, smtp_passwd

# メッセージオブジェクトをつくる関数
def create_message(frm, to, subject, plain, html):
	msg = MIMEMultipart("alternative")
	msg["Subject"] = subject
	msg["From"] = frm
	msg["To"] = to
	msg["Date"] = formatdate()
	pm = MIMEText(plain)
	msg.attach(pm)
	hm = MIMEText(html, "html")
	msg.attach(hm)
	return msg

# SMTPサーバーを通してメールを送る関数
def smtp_send(host, port, user, password, mailfrom, mailtos, messages):
	if len(messages) == 0:
		return
	with SMTP_SSL(host, port) as smtp:
		smtp.login(user, password)
		for message in messages:
			smtp.sendmail(mailfrom, mailtos, message.as_string())

# 複数のメールを設定に基づいて送信する
def send(mails):
	mail_tos = [t.strip() for t in mail_to.split(",") if t.strip()]
	messages = [create_message(mail_from, mail_to, subject, plain, html) for subject, plain, html in mails]
	smtp_send(smtp_host, smtp_port, smtp_user, smtp_passwd, mail_from, mail_tos, messages)

# 通知配信を制限に則って行うクラス
class NotificationController():

	# コンストラクタ
	def __init__(self, max_per_hour, dry=False):
		self.count = 0
		self.hour = datetime.datetime.now().strftime("%Y-%m-%d %H")
		self.max_per_hour = max_per_hour
		self.dry = dry

	# 時間あたりの最大件数を超えない数にリストをスライスして状態を更新
	def filter(self, items):
		hour = datetime.datetime.now().strftime("%Y-%m-%d %H")
		if self.hour != hour:
			self.hour = hour
			self.count = 0
		num = min(len(items), self.max_per_hour - self.count)
		self.count += num
		return items[0:num]

	# 複数のメールを設定に基づいて時間あたりの最大件数を超えないように送信する
	def send(self, mails):
		mails = self.filter(mails)
		if not self.dry:
			send(mails)
		return len(mails)

	# 設定に基づいて時間あたりの最大件数を超えない数のアイテムでフックを実行する
	def run_hook(self, hook, items):
		items = self.filter(items)
		if not self.dry:
			hook(items)
		return len(items)
