import os
import configparser
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

# カレントディレクトリ変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# メール関係の設定
config = configparser.SafeConfigParser()
config.read("settings.ini")
email = config.get("general", "email")
bcc = config.get("general", "bcc")
smtp = config.get("general", "smtp")
port = int(config.get("general", "port"))
efrom = config.get("general", "from")
user = config.get("general", "user")
password = config.get("general", "password")

# メール文字列をつくる
def create_message(efrom, to, bcc, subject, body):
	msg = MIMEText(body)
	msg["Subject"] = subject
	msg["From"] = efrom
	msg["To"] = to
	msg["Bcc"] = bcc
	msg["Date"] = formatdate()
	return msg

# SMTPサーバーを通してメールを送る
def send(smtp, port, user, password, efrom, to, msg):
	smtpobj = smtplib.SMTP_SSL(smtp, port)
	smtpobj.login(user, password)
	smtpobj.sendmail(efrom, to, msg.as_string())
	smtpobj.quit()

# テストメール送信
subject = "Ziraffem Test Mail"
body = "Ziraffem mailing works!"
msg = create_message(efrom, email, bcc, subject, body)
send(smtp, port, user, password, efrom, email, msg)
