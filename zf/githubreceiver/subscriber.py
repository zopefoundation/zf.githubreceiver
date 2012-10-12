##############################################################################
#
# Copyright (c) 2012 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import logging

from githubevent.events import Push
from pyramid.events import subscriber

from zf.githubreceiver.commit_email import send_email
from zf.githubreceiver.commit_log import log_push


logger = logging.getLogger('githubreceiver')


@subscriber(Push)
def handle_push(event):
    push = event.request.json_body

    if ( push['pusher']['name'] == 'none' and
         push['pusher'].get('email', None) is None ):
        # Special case: Someone is using the test push hook button
        logger.info('Web hook test button pressed on GitHub')
        return

    log_push(event.request)

    if len(push['commits']) > 40:
        # safeguard against github getting confused and sending us 
        # the entire history
        logger.warn('Received too many commits in this push!')
        return

    for commit in push['commits']:
        send_email(push, commit, event.request)

