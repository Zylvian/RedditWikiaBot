import praw
from prawoauth2 import PrawOAuth2Server

scopes = ['identity', 'read', 'submit', 'privatemessages']
app_key='g1vTSghKvgXGcg'
app_secret='WBqF5fei1-GWtua3CVjyKeJmpCk'
user_agent = 'One Piece Wiki bot 0.1'
reddit_client = praw.Reddit(user_agent=user_agent)
oauthserver = PrawOAuth2Server(reddit_client, app_key, app_secret,
                               state=user_agent, scopes=scopes)

oauthserver.start()