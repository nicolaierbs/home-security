from twilio.rest import Client
import configparser

config_section = 'TWILIO'
params = configparser.ConfigParser()
params.read('parameters.ini')

account_sid = params.get(config_section, 'account_sid')
auth_token = params.get(config_section, 'auth_token')


def send_whatsapp(message):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to='whatsapp:+491636375636'
    )
    return message.sid
