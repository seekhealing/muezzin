import logging
logger = logging.getLogger(__name__)

import os
from email.mime.text import MIMEText
from email import encoders
import base64

from jinja2 import Template
from httplib2 import Http
from googleapiclient.discovery import build
from googleapiclient import errors
from oauth2client import file, client, tools
import arrow

SCOPES = 'https://www.googleapis.com/auth/gmail.send'


class Email(object):
    def __init__(self, template=os.path.join(os.path.dirname(__file__), 'email.j2'),
                 secrets_file=os.path.join(os.path.dirname(__file__), 'credentials.json')):
        self.template = template
        self.secrets_file = secrets_file
        self.api = self.__api__()
        
    def __api__(self):
        store = file.Storage(os.path.join(os.path.dirname(__file__), 'gmail-token.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.secrets_file, SCOPES)
            creds = tools.run_flow(flow, store)
        return build('gmail', 'v1', http=creds.authorize(Http()))

    def send(self, seeker_name, seeker_email, events, dry_run=False):
        tmpl = Template(open(self.template).read())
        body = tmpl.render(seeker=seeker_name, email=seeker_email, events=events)
        message = MIMEText(body)        

        message['to'] = seeker_email
        message['from'] = 'info@seekhealing.org'
        message['subject'] = 'Upcoming SeekHealing Events - %s' % (arrow.now().format('ddd, MMM D'))
        payload = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('ascii')}
        try:
            logger.info('Sending email to %s', seeker_email)
            if dry_run:
                logger.debug('%s', body)
            else:
                self.api.users().messages().send(userId='me', body=payload).execute()
        except errors.HttpError as e:
            logger.exception('Error communicating with Gmail!')


