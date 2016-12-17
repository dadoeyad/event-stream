# Setup
1. Install requirments `pip install -r requirements.txt`
2. Get Consumer Key, Consumer Secret, Access Token, Access Token Secret from your twitter app and export the keys in you env
```
export TWITTER_APP_KEY='Consumer-Key'
export TWITTER_APP_SECRET='Consumer-Secret'
export TWITTER_ACCESS_TOKEN='Access-Token'
export TWITTER_ACCESS_TOKEN_SECRET='Access-Token-Secret'
```
4. Create s Slack bot, add it to a public channel, get API token and export in your env
```
export SLACK_BOT_TOKEN='slack-API-token'
```
5. Export a Django secert key in env
```
export SECRET_KEY='Django-secert-key'
```

# Run
`./manage.py`

# TODO
* Deploy to Heroku
* Review if it's better to use Slack Outgoing WebHooks over RTM API
* Get and implement a design
