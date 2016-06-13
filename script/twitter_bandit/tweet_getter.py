from requests_oauthlib import OAuth1Session
import json

class TweetGetter():
    def __init__(self, consumer_key, consumer_secret, 
                 access_token, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    def get_tweet(self, username, count = 10):
        twitter = OAuth1Session(self.consumer_key, self.consumer_secret,
                                self.access_token, self.access_secret)
        params = {"screen_name": username, "count":count}
        req = twitter.get(self.url, params = params)
        if req.status_code == 200:
            tweets = json.loads(req.text)
            return tweets
        else:
            print ("error in getting {}'s tweet".format(username))
            return None
    
