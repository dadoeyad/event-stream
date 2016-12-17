import json
import logging
import requests
from threading import Thread, Lock

from django.conf import settings
from channels import Group

from slacksocket import SlackSocket as LibSlackSocket
from slacksocket.models import SlackEvent

log = logging.getLogger(__name__)


class SlackSocket(LibSlackSocket):

    def __init__(self, slacktoken, translate=True, event_filters='all'):
        if type(translate) != bool:
            raise TypeError('translate must be a boolean')
        self._validate_filters(event_filters)

        self._eventq = []
        self._sendq = []
        self.connected = False
        self._translate = translate
        self.event_filters = event_filters

        self._requests = requests.Session()
        self._slacktoken = slacktoken
        self.team, self.user = self._auth_test()

        # used while reading/updating loaded_user property
        self.load_user_lock = Lock()
        self._load_users()
        self.loaded_channels = {}
        # used while reading/updating loaded_channels property
        self.load_channel_lock = Lock()
        self._load_channels()

    def set_group(self):
        self._group = Group('slack')

    def start(self):
        self._thread = Thread(target=self._open)
        self._thread.daemon = True
        self._thread.start()
        self.running = True

    def _find_user_name(self, user_id):
        """
        rewrite to return username and image
        """
        self.load_user_lock.acquire()
        try:
            users = self.loaded_users
        finally:
            self.load_user_lock.release()

        for user in users:
            if user['id'] == user_id:
                return {
                    'username': user['name'],
                    'img': user['profile']['image_32']
                }

    def _event_handler(self, ws, event_json):
        log.debug('event recieved: %s' % event_json)

        json_object = json.loads(event_json)

        if self.event_filters != "all" and json_object.get("type") not in self.event_filters:
            log.debug("Ignoring the event {} as it not matching event_filers {}"
                      .format(event_json, self.event_filters))
            return

        event = SlackEvent(json_object)

        if self._translate:
            event = self._translate_event(event)

        message = {
            'text': json.dumps({
                'text': event.event['text'],
                'img': event.event['user']['img'],
                'username': event.event['user']['username'],
            })
        }
        self._group.send(message)

    def disconnect(self):
        self.close()


slack = SlackSocket(settings.SLACK_BOT_TOKEN, translate=True, event_filters=['message'])
