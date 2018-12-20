import logging
logger = logging.getLogger(__name__)

import os

def run(test=False, dry_run=False, templates_dir='',
        send_email=True, send_sms=True, days_ahead=4,
        calendar_url=None, calendar_name=None):
    from . import seekers, calendar, email, sms, facebook
    if test:
        logger.info('Test mode enabled. Only processing seekers with last name Testerson.')
    seekers = seekers.Seekers()
    cal_kwargs = dict(days_ahead=days_ahead)
    if calendar_url:
        cal_kwargs['url'] = calendar_url
    if calendar_name:
        cal_kwargs['name'] = calendar_name
    events = calendar.EventList(**cal_kwargs)
    if not events:
        logging.info('No events')
        return
    email_kwargs = {'template': os.path.join(templates_dir, 'email.j2')} if templates_dir else {}
    email = email.Email(**email_kwargs)
    sms_kwargs = {'template': os.path.join(templates_dir, 'sms.j2')} if templates_dir else {}
    sms = sms.SMS(**sms_kwargs)
    facebook = facebook.Facebook()
    for seeker_name, seeker_comms_pref, seeker_contact in seekers:
        test_case = seeker_name.rsplit(' ', 1)[-1] == 'Testerson'
        if test != test_case:
            continue
        logger.debug('Seeker: %s; Comms pref: %s', seeker_name, seeker_comms_pref)
        if seeker_comms_pref == 'Email' and send_email:
            email.send(seeker_name, seeker_contact, events, dry_run=dry_run)
        elif seeker_comms_pref == 'SMS' and send_sms:
            sms.send(seeker_name, seeker_contact, events, dry_run=dry_run)
        elif seeker_comms_pref == 'Facebook':
            logger.info('Facebook presently disabled...')
            # facebook.send(seeker_name, seeker_contact, events)

if __name__ == '__main__':
    run()
