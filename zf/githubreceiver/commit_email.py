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

import os

from chameleon import PageTemplateLoader
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
import requests


TMPLS = PageTemplateLoader(os.path.join(os.path.dirname(__file__), "templates"))
ADDED_RECIPIENTS = {
    'CMF' : ['cmf-checkins@zope.org'],
    'CMF_Extras' : ['cmf-checkins@zope.org'],
    'CMF_Hotfixes' : ['cmf-checkins@zope.org'],
    'Products.Five' : ['zope-checkins@zope.org'],
    'Zope': ['zope-checkins@zope.org'],
    'Zope3': ['zope3-checkins@zope.org'],
    'zope.testing': ['zope3-checkins@zope.org'],
    'zope.formlib': ['zope3-checkins@zope.org'],
    'ldapauth': ['zope3-checkins@zope.org'],
    'messageboard': ['zope3-checkins@zope.org'],
    'zodbbench': ['zodb-checkins@zope.org'],
    'ZODB': ['zodb-checkins@zope.org'],
    'ZConfig': ['zconfig@zope.org'],
    'zdaemon': ['zope-checkins@zope.org',
                'zope3-checkins@zope.org',
                'zodb-checkins@zope.org'],
    'zpkgtools': ['zpkg@zope.org'],
    'pushtest': ['jens@zetwork.com'],
}


def send_email(push, commit, request):
    mailer = get_mailer(request)
    settings = request.registry.settings
    commitwarning = None
    repository = push['repository']['name']
    pusher_email = push['pusher'].get('email', '')

    if pusher_email != commit['author']['email']:
        # Pusher != Committer, do stuff
        commitwarning = 'Code author and pusher do not match!'

    short_commit_msg = commit['message'].split('\n')[0][:60]
    reply_to = '%s <%s>' % (commit['author']['name'], commit['author']['email'])
    diff = requests.get(commit['url'] + '.diff').content
    
    files = ['A %s' % f for f in commit['added']]
    files.extend('M %s' % f for f in commit['modified'])
    files.extend('D %s' % f for f in commit['removed'])

    data = {
        'push': push,
        'commit': commit,
        'files': '\n'.join(files),
        'diff': diff,
        'commitwarning': commitwarning,
        'pusher_email': pusher_email
    }

    recipients = ["%s" % settings['recipient_email']]
    if repository in ADDED_RECIPIENTS:
        recipients.extend(ADDED_RECIPIENTS[repository])

    msg = Message(
        subject = '%s/%s: %s' % ( repository
                                , push['ref'].split('/')[-1]
                                , short_commit_msg
                                ),
        sender = "%s <%s>" % ( commit['author']['name']
                             , settings['sender_email']
                             ),
        recipients = recipients,
        body = TMPLS['commit_email.pt'](**data),
        extra_headers = {'Reply-To': reply_to}
        )
    
    mailer.send(msg)

    if pusher_email != commit['author']['email']:
        # Warn the committer - he may not be aware of the commit
        msg = Message(
            subject = '%s/%s: %s' % ( repository
                                    , push['ref'].split('/')[-1]
                                    , short_commit_msg
                                    ),
            sender="Zope Foundation contributor committee <contributor-admin@zope.org>",
            recipients = [commit['author']['email']],
            body = TMPLS['committer_warning.pt'](**data),
            )
        
        mailer.send(msg)

