import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import configparser


config_section = 'GMAIL'
config = configparser.ConfigParser()
config.read('parameters.ini')

user = config.get(config_section, 'user')
password = config.get(config_section, 'password')
sender = config.get(config_section, 'sender')
recipients = config.get(config_section, 'recipients')


def send_mail(content, image_path):

    msg = MIMEMultipart()
    msg['Subject'] = content
    msg['From'] = sender
    msg['To'] = recipients
    msg.preamble = 'Fahrstuhlkamera'

    with open(image_path, 'rb') as fp:
        img = MIMEImage(fp.read())
        msg.attach(img)

    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(user, password)  # login with mail_id and password

    session.sendmail(user, recipients.split(","), msg.as_string())
    session.quit()

