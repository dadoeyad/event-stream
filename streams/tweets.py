import tweepy

from django.conf import settings

from channels import Group


auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class TweetsListener(tweepy.StreamListener):

    def set_group(self):
        self._group = Group('tweets')

    def on_status(self, status):
        tweet = {
            'text': status.text
        }
        self._group.send(tweet)


tweets_listener = TweetsListener()
tweets = tweepy.Stream(auth=api.auth, listener=tweets_listener)
