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
            <li>Vender: {}</li>
            <li>Card Model: {}</li>
            <li>Availability: {}</li>
            <li>Price: {}</li>
            <li>Purchase Link: {}</li>
        </ul>
        -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    </div>
    '''.format(vender,card_model,availability, price,link)
    return msg

def create_message_with_attachment(sender, to, subject, message_text, file):
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'

  main_type, sub_type = content_type.split('/', 1)

  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read().decode("utf-8"), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {'raw': raw_message.decode("utf-8")}


def email(service,message):
    for name in EMAILS:
        msg = create_message('stevewflores43@gmail.com', name, 'RTX 2080 AVAILABILITY/PRICES',message)
        send_msg = send_message(service, 'me', msg)
        print("messages sent: %s" % send_msg)


if __name__ == "__main__":
    service = Service()
    email(service,'test')
