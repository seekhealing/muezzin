import logging
logger = logging.getLogger(__name__)

import os
from email.mime.text import MIMEText
from email import encoders
import base64
import pickle

from jinja2 import Template
from httplib2 import Http
from googleapiclient.discovery import build
from googleapiclient import errors
from google.auth.transport.requests import Request
import arrow

SCOPES = 'https://www.googleapis.com/auth/gmail.send'


class Email(object):
    def __init__(self, template=os.path.join(os.path.dirname(__file__), 'email.j2'),
                 subject=None):
        self.template = template
        self.subject = subject
        self.api = self.__api__()
        
    def __api__(self):
        if os.environ.get('GOOGLE_TOKEN'):
            self.token = pickle.loads(base64.decodebytes(os.environ('GOOGLE_TOKEN')))
        else:
            token_file = os.path.join(os.path.dirname(__file__), 'token.pickle')
            self.token = pickle.load(open(token_file, 'rb'))
        if not self.token or not self.token.valid:
            if self.token and self.token.expired and self.token.refresh_token:
                self.token.refresh(Request())
            else:
                raise ValueError('Token is not valid.')
        return build('gmail', 'v1', credentials=self.token)

    def send(self, seeker_name, seeker_email, events, dry_run=False):
        tmpl = Template(open(self.template).read())
        body = tmpl.render(seeker=seeker_name, email=seeker_email, events=events)
        message = MIMEText(body)        

        message['to'] = seeker_email
        message['from'] = 'info@seekhealing.org'
        message['subject'] = self.subject or 'Upcoming %s - %s' % (events.name, arrow.now().format('ddd, MMM D'))
        payload = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('ascii')}
        try:
            logger.info('Sending email to %s', seeker_email)
            if dry_run:
                logger.debug('%s', body)
            else:
                self.api.users().messages().send(userId='me', body=payload).execute()
        except errors.HttpError as e:
            logger.exception('Error communicating with Gmail!')


