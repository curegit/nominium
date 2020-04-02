import smtplib
from email.utils import formatdate
from email.mime.text import MIMEText

# メール文字列をつくる関数
def create_message(mailfrom, mailto, bcc, subject, body):
	msg = MIMEText(body)
	msg["Subject"] = subject
	msg["From"] = mailfrom
	msg["To"] = mailto
	msg["Bcc"] = bcc
	msg["Date"] = formatdate()
	return msg

# SMTP サーバーを通してメールを送る関数
def smtp_send(host, port, user, password, mailfrom, mailto, msg):
	smtpobj = smtplib.SMTP_SSL(host, port)
	smtpobj.login(user, password)
	smtpobj.sendmail(mailfrom, mailto, msg.as_string())
	smtpobj.quit()

# メールを送る関数を作成する関数
def make_sendmail(host, port, user, password, mailfrom, mailto):
	def sendmail(subject, body):
		msg = create_message(mailfrom, mailto, bcc, subject, body)
		smtp_send(host, port, user, password, mailfrom, mailto, msg)
	return sendmail
