import logging

from githubevent.events import Push
from pyramid.events import subscriber

from zf.githubreceiver.commit_email import send_email


logger = logging.getLogger('githubreceiver')


@subscriber(Push)
def handle_push(event):
    push = event.request.json_body
    logger.info(push)

    if len(push['commits']) > 40:
        # safeguard against github getting confused and sending us 
        # the entire history
        logger.warn('Received too many commits in this push!')
        return

    for commit in push['commits']:
        send_email(push, commit, event.request)

