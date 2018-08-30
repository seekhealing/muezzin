import os

import requests
from jinja2 import Template

ACCESS_TOKEN = open(os.path.join(os.path.dirname(__file__), 'fb-token.txt')).read()

class Facebook(object):
    def send(self, seeker_name, seeker_fbid, events):
        tmpl = Template(open(os.path.join(os.path.dirname(__file__), 'facebook.j2')).read())
        body = tmpl.render(seeker=seeker_name, events=events)

        try:
            response = requests.post(
                'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN,
                json={
                    'messaging_type': 'UPDATE',
                    'recipient': {
                        'id': str(seeker_fbid),
                    },
                    'message': {
                        'text': body
                    }
                }
            )
            print(response.status_code)
            print(response)
            response.raise_for_status()
        except requests.RequestException as e:
            print(e)

