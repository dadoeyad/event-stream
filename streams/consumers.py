import logging

from django.conf import settings
from channels import Group
from channels.sessions import channel_session

from .tweets import tweets
from slack import slack

log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    try:
        prefix, label = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'streams':
            log.debug('invalid ws path=%s', message['path'])
            return
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return

    log.debug('stream connect to label=%s', label)

    Group(label).add(message.reply_channel)

    message.channel_session['label'] = label

    if label == 'tweets':
        tweets.listener.set_group()
        tweets.filter(track=settings.LISTENER_WORDS, async=True)
    elif label == 'slack':
        slack.set_group()
        slack.start()
    else:
        log.warning('unknown label=%s', label)
        return


@channel_session
def ws_disconnect(message):
    try:
        prefix, label = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'streams':
            log.debug('invalid ws path=%s', message['path'])
            return
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return

    log.debug('stream disconnect to label=%s', label)

    Group(label).discard(message.reply_channel)

    if label == 'tweets':
        tweets.disconnect()
    elif label == 'slack':
        slack.disconnect()
    else:
        log.warning('unknown label=%s', label)
        return
