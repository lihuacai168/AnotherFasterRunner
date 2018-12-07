import smtplib

from email.header import Header
from email.mime.text import MIMEText
from django.conf import settings


def sendEmail(title, content, receivers):
    message = content  # 内容, 格式, 编码
    message['From'] = settings.MAIL_INFO('mail_from')
    message['To'] = ",".join(receivers)
    message['Subject'] = Header(title, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(settings.MAIL_INFO('mail_host'), 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(settings.MAIL_INFO('mail_user'), settings.MAIL_INFO('mail_pass'))  # 登录验证
        smtpObj.sendmail(settings.MAIL_INFO('sender'), receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)
