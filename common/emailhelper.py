import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE
from email import encoders
import os

import config

smtp_host = 'smtp.exmail.qq.com'
smtp_sender = 'zhsf@zehuiguoxue.com'
smtp_password = 'opp885rhpttd273g'

'''
html:内容
subject: 主题
receivers:接收者，类型字符串，例子：xx@xx.xx  list
'''
def send_email(receivers, subject, html):
    if not isinstance(receivers, list):
        receivers = [receivers]

    content_message = MIMEText(html, 'HTML', 'utf-8')
    message = MIMEMultipart()
    message.attach(content_message)
    message['From'] = smtp_sender
    message['To'] = COMMASPACE.join(receivers)
    message['Subject'] = subject
    smtp = smtplib.SMTP_SSL(host=smtp_host, port=465)
    smtp.login(smtp_sender, smtp_password)
    result = smtp.sendmail(smtp_sender, receivers, message.as_string())
    smtp.quit()
    return result
