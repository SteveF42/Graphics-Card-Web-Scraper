from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.audio import MIMEAudio
import mimetypes
import os
from GmailAPI import Service
import base64

EMAILS = ['stevewflores43@gmail.com']

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text,'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
    'raw': raw_message.decode("utf-8")
    }



def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(
            userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None

def format_message(products):
    card_model = products['card_name']
    availability = products['availability']
    price = products['price']
    link = products['link']
    vender = products['vender']

    msg = '''
    <div>
        <ul> 
            <li>Vender: <strong>{}</strong> </li>
            <li>Card Model: <strong>{}</strong> </li>
            <li>Availability: <strong>{}</strong> </li>
            <li>Price: <strong>{}</strong> </li>
            <li>Purchase Link: {} </li>
        </ul>
        -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    </div>
    '''.format(vender,card_model,availability, price,link)
    return msg



def email(service,message):
    for name in EMAILS:
        msg = create_message('me', name, 'RTX 2080 AVAILABILITY/PRICES',message)
        send_msg = send_message(service, 'me', msg)
        print("messages sent: %s" % send_msg)


if __name__ == "__main__":
    service = Service()
    email(service,'test')
