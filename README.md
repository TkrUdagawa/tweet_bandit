#Tweet Bandit Demo

This is an example of recommending the tweets by jubabandit.

##How to Try

### Set your twitter keys
Open config/access_token.json with any text editor and write your consumer key, consumer secret, access token and access secret.

### Install python packages
```
cd script/
python setup.py install 
```

### Launch demo servers
```
./start_demo.sh ../config/jubabandit.conf
```

### Access server
Access http://localhost:9000 with a web browser.

### Get recommended Tweets
Push the select_arm button in the page and some tweets will be displayed in a few second.
Those are recommended tweets for you by bandit algorithm.

### Return feedback
Click on the any tweet you like. This action means you like the tweets.
This feedback will be sent to bandit servers and those servers will be rewarded.

You can repeat this get tweets and return feedback process anytime you want.

## Configuration
###config/jubabandit.conf
This config file is for jubabandit servers.
You can set the algorithm and parameters used in the system.
See [Jubatus official website](http://jubat.us/ja/api_bandit.html)

###config/config.json
This config file specifies which categories and what twitter users is used in recommendation.
And also jubatus servers' ports are set in this config.
Its structure is like below:

```
{
  "port": 9300, #this port is used for category choose bandit
  "category": {
    "category 1" {
      "port": 9301,  # you have to specify the jubatus server's port number
      "user": [      # write twitter account names
        "user_A",
        "user_B",
	...
      ]
    }
    ...

    # You can add as many category as you like.
    
  }
}
```

