import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import configparser
from prettytable import PrettyTable


config_section = 'GMAIL'
config = configparser.ConfigParser()
config.read('parameters.ini')

user = config.get(config_section, 'user')
password = config.get(config_section, 'password')
sender = config.get(config_section, 'sender')
recipients = config.get(config_section, 'recipients')


def create_body(parameters):

    tabular_table = PrettyTable()
    tabular_table.field_names = ["Parameter", "Value"]
    for parameter in parameters.items():
        tabular_table.add_row([parameter[0], parameter[1]])

    html = """\
    <html>
        <head>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
                text-align: left;    
            }    
        </style>
        </head>
    <body>
    <p>Status:<br>
       %s
    </p>
    </body>
    </html>
    """ % (tabular_table.get_html_string())
    return html


def send_mail(parameters, image_path):

    msg = MIMEMultipart()
    msg['Subject'] = 'Fahrstuhl Update'
    msg['From'] = sender
    msg['To'] = recipients
    msg.preamble = 'Fahrstuhlkamera'

    part1 = MIMEText(str(parameters), 'plain')
    part2 = MIMEText(create_body(parameters), 'html')

    with open(image_path, 'rb') as fp:
        img = MIMEImage(fp.read(), subtype='jpg')
        msg.attach(img)

    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(user, password)  # login with mail_id and password

    session.sendmail(user, recipients.split(","), msg.as_string())
    session.quit()

