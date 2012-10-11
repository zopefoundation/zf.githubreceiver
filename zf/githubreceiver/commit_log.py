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
                , push['pusher']['email']
                , [x['id'] for x in commits]
                )
    logger.info(push_msg % push_data)

    for commit in commits:
        commit_data = ( commit['id']
                      , commit['author']['username']
                      , commit['author']['email']
                      , commit['url']
                      )

        if commit['author']['email'] != push['pusher']['email']:
            logger.warn(commit_msg % commit_data)
        else:
            logger.info(commit_msg % commit_data)

