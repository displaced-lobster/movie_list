import os
import httplib2
import base64

from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools
from apiclient import discovery

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib import error

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = '../client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'

def create_message(sender, to, subject, message_text, message_html):
    message = MIMEMultipart('alternative')
    message['to'] = ', '.join(to)
    message['from'] = sender
    message['subject'] = subject
    part1 = MIMEText(message_text, 'plain')
    part2 = MIMEText(message_html, 'html')
    message.attach(part1)
    message.attach(part2)
    return{'raw' : base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: ', message['id'])
        return message
    except error.HTTPError:
        print('An error occurred: ', error.HTTPError)

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to', credential_path)
    return credentials

def create_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service

def email(sender, to, subject, text, html):
    service = create_service()
    message = create_message(sender, to, subject, text, html)
    send_message(service, 'me', message)
