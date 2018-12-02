import logging
logger = logging.getLogger(__name__)

import os
import datetime
import collections

from icalevents import icalevents
import arrow
import requests

CALENDAR_URL = open(os.path.join(os.path.dirname(__file__), 'gcal-url.txt')).read()

class EventList(collections.UserList):
    def __init__(self, data=[], url=CALENDAR_URL, days_ahead=4):
        self.url = url
        self.days_ahead = days_ahead
        self.__events__ = data
    
    def in_range(self, event, event_horizon):
        if arrow.utcnow() < event.start < event_horizon:
            logger.debug('Event %s is in range - start %s, event_horizon %s',
                         event.summary, event.start, event_horizon)
            return True
        else:
            #logger.debug('Event %s out of range - start %s, event_horizon %s',
            #             event.summary, event.start, event_horizon)
            return False

    @property
    def data(self):
        event_horizon = arrow.utcnow() + datetime.timedelta(days=self.days_ahead)
        if not self.__events__:
            logger.info('Getting events from Google Calendar between now and %s.', event_horizon)
            try:
                self.__events__ = icalevents.events(self.url)
                self.__events__.sort(key=lambda e: e.start)
            except Exception:
                logger.exception('Error getting calendar!')
                raise
        return [Event(event) for event in self.__events__ if self.in_range(event, event_horizon)]

class Event(object):
    def __init__(self, icalevent):
        self.name = icalevent.summary
        self.begin = arrow.Arrow.fromdatetime(icalevent.start.replace(tzinfo=None))
        self.end = arrow.Arrow.fromdatetime(icalevent.end.replace(tzinfo=None))
        self.description = getattr(icalevent, 'description', '')
        self.location = icalevent.location