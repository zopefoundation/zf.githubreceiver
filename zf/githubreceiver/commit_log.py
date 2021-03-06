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
import operator


logger = logging.getLogger('GitHub')

def log_push(request):
    push = request.json_body
    commits = push['commits'][:]
    commits.sort(key=operator.itemgetter('timestamp'))

    #logger.info(push)

    push_msg = 'PUSH to %s/%s by %s (%s) %s'
    commit_msg = 'COMMIT %s by %s (%s): %s'

    push_data = ( push['repository']['name']
                , push['ref'].split('/')[-1]
                , push['pusher']['name']
                , push['pusher'].get('email', 'unknown email')
                , [x['id'] for x in commits]
                )
    logger.info(push_msg % push_data)

    for commit in commits:
        commit_data = ( commit['id']
                      , commit['author']['username']
                      , commit['author']['email']
                      , commit['url']
                      )

        if commit['author']['email'] != push['pusher'].get('email'):
            logger.warn(commit_msg % commit_data)
        else:
            logger.info(commit_msg % commit_data)

