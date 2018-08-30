import logging
logger = logging.getLogger(__name__)

def run(test=False, dry_run=False):
    from . import seekers, calendar, email, sms, facebook
    if test:
        logger.info('Test mode enabled. Only processing seekers with last name Testerson.')
    seekers = seekers.Seekers()
    events = calendar.EventList()
    if not events:
        logging.info('No events')
        return
    email = email.Email()
    sms = sms.SMS()
    facebook = facebook.Facebook()
    for seeker_name, seeker_comms_pref, seeker_contact in seekers:
        test_case = seeker_name.rsplit(' ', 1)[-1] == 'Testerson'
        if test != test_case:
            continue
        logger.debug('Seeker: %s; Comms pref: %s', seeker_name, seeker_comms_pref)
        if seeker_comms_pref == 'Email':
            email.send(seeker_name, seeker_contact, events, dry_run=dry_run)
        elif seeker_comms_pref == 'SMS':
            sms.send(seeker_name, seeker_contact, events, dry_run=dry_run)
        elif seeker_comms_pref == 'Facebook':
            logger.info('Facebook presently disabled...')
            # facebook.send(seeker_name, seeker_contact, events)

if __name__ == '__main__':
    run()
