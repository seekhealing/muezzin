import logging
logger = logging.getLogger(__name__)

import os
import pickle
import base64

from googleapiclient.discovery import build
from googleapiclient import errors
from google.auth.transport.requests import Request

SPREADSHEET_ID = '1JGpgxAdBSWK5iQ9D4wXxCUynLI6LueuBaMRkl4qW7K8'
RANGE = 'Sheet1!A1:C'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

class Seekers(object):
    def __init__(self, spreadsheet_id=SPREADSHEET_ID, range=RANGE, 
                 secrets_file=os.path.join(os.path.dirname(__file__), 'credentials.json')):
        self.spreadsheet_id = spreadsheet_id
        self.range = range
        self.secrets_file = secrets_file

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
        return build('sheets', 'v4', credentials=self.token)

    def __iter__(self):
        api = self.__api__()
        logger.info('Accessing seekers from Google Sheets.')
        try:
            result = api.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, 
                                                 range=self.range).execute()
        except Exception:
            logger.exception('Error getting seeker sheet!')
            raise
        seekers = result.get('values', [(), (),])
        _, _, service_enabled = seekers.pop(0)
        logger.debug('Service enabled? %s', service_enabled)
        if service_enabled != 'TRUE':
            logger.warning('Service has been disabled in spreadsheet. Discontinuing.')
            return None
        _ = seekers.pop(0)
        for value in result.get('values', []):
            if value[0] and value[1] and value[2]:
                yield value
            else:
                logger.debug('Skipped row for blank entry: %s', str(value))
