from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib


def send_email(page_name,vol,context):
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "mwslatvia@gmail.com"  # Enter your address
        receiver_email = context.config.userdata.get("emailReceiver")  # Enter receiver address
        password = "phqxnklfmniqnodu"
        message = MIMEMultipart("alternative")
        message["Subject"] = "Daily report from: "+page_name
        message["From"] = sender_email
        message["To"] = receiver_email
        text = ""
        message.attach(MIMEText(text.join(vol), 'html', 'utf-8'))
        if len(vol) > 0:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()   # optional
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        # ...send emails
    except smtplib.SMTPException as e:
        print('Something went wrong...'+e)
