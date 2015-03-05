from twython import Twython

APP_KEY = raw_input('app key: ')
APP_SECRET = raw_input('app secret: ')

twitter = Twython(APP_KEY, APP_SECRET)

auth = twitter.get_authentication_tokens()

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

print auth['auth_url']

OAUTH_VERIFIER = raw_input("verification code: ")

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

auth = twitter.get_authorized_tokens(OAUTH_VERIFIER)

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

print 'OAUTH_TOKEN=\'%s\'' % OAUTH_TOKEN
print 'OAUTH_TOKEN_SECRET=\'%s\'' % OAUTH_TOKEN_SECRET