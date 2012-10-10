import os
import logging
import requests
from pyramid.events import subscriber
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from githubevent.events import Push
from chameleon import PageTemplateLoader

logger = logging.getLogger('githubreceiver')
templates = PageTemplateLoader(os.path.join(os.path.dirname(__file__), "templates"))


@subscriber(Push)
def handle_push(event):
    push = event.request.json_body
    logger.info(push)
    mailer = get_mailer(event.request)
    settings = event.request.registry.settings

    if len(push['commits']) > 40:
        # safeguard against github getting confused and sending us the entire history
        return

    for commit in push['commits']:
        commitwarning = None

        if push['pusher']['email'] != commit['author']['email']:
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
        }

        msg = Message(
            subject = '%s/%s: %s' % (push['repository']['name'],
                                 push['ref'].split('/')[-1],
                                 short_commit_msg),
            sender = "%s <%s>" % ( commit['author']['name']
                                 , settings['sender_email']
                                 ),
            recipients = ["%s" % settings['recipient_email']],
            body = templates['commit_email.pt'](**data),
            extra_headers = {'Reply-To': reply_to}
            )
        
        mailer.send(msg)

