import logging
logger = logging.getLogger(__name__)

import os

import requests
from jinja2 import Template

API_USERNAME = 'ACcb87d18fe15bee722b834de0df2da1ee'
API_PASSWORD = open(os.path.join(os.path.dirname(__file__), 'sms-password.txt')).read()

class SMS(object):
    def __init__(self, template=os.path.join(os.path.dirname(__file__), 'sms.j2')):
        self.template = template

    def normalize_number(self, seeker_number):
        return '+1' + ''.join([c for c in seeker_number if c in '01234568789'])[-10:]

    def send(self, seeker_name, seeker_number, events, dry_run=False):
        tmpl = Template(open(self.template).read())
        body = tmpl.render(seeker=seeker_name, number=seeker_number, events=events)
        try:
            logger.info('Sending SMS to %s', self.normalize_number(seeker_number))
            if not dry_run:
                response = requests.post(
                    'https://api.twilio.com/2010-04-01/Accounts/ACcb87d18fe15bee722b834de0df2da1ee/Messages.json',
                    data={'To': self.normalize_number(seeker_number),
                        'From': '+18285154758',
                        'Body': body},
                    auth=requests.auth.HTTPBasicAuth(username=API_USERNAME,
                                                    password=API_PASSWORD))
                response.raise_for_status()
        except requests.RequestException as e:
            logger.exception('Error communicating with Twilio!')