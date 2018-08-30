import logging
logger = logging.getLogger(__name__)

import os

from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client import file, client, tools

SPREADSHEET_ID = '1JGpgxAdBSWK5iQ9D4wXxCUynLI6LueuBaMRkl4qW7K8'
RANGE = 'Sheet1!A2:C'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

class Seekers(object):
    def __init__(self, spreadsheet_id=SPREADSHEET_ID, range=RANGE, 
                 secrets_file=os.path.join(os.path.dirname(__file__), 'credentials.json')):
        self.spreadsheet_id = spreadsheet_id
        self.range = range
        self.secrets_file = secrets_file

    def __api__(self):
        store = file.Storage(os.path.join(os.path.dirname(__file__), 'gcal-token.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.secrets_file, SCOPES)
            creds = tools.run_flow(flow, store)
        return build('sheets', 'v4', http=creds.authorize(Http()))

    def __iter__(self):
        api = self.__api__()
        logger.info('Accessing seekers from Google Sheets.')
        try:
            result = api.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, 
                                                 range=self.range).execute()
        except Exception:
            logger.exception('Error getting seeker sheet!')
            raise
        for value in result.get('values', []):
            if value[0] and value[1] and value[2]:
                yield value
            else:
                logger.debug('Skipped row for blank entry: %s', str(value))
