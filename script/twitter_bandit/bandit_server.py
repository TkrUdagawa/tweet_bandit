# -*- coding:utf-8 -*-

import sys,json,os
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import httpserver
from twitter_bandit.bandit_client import TwitterBanditClient
from twitter_bandit.tweet_getter import TweetGetter

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class BanditHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("web socket opend")
        bandit_client = TwitterBanditClient(category_port = TornadoApp.category_port, 
                                            categories = TornadoApp.categories, 
                                            ports = TornadoApp.ports)
        bandit_client.initialize_arms(TornadoApp.json_config)

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print (message)
        bandit_client = TwitterBanditClient(category_port = TornadoApp.category_port, 
                                            categories = TornadoApp.categories, 
                                            ports = TornadoApp.ports)
        json_message = json.loads(message)
        message_type = json_message["type"]
        
        if message_type == "select":
            tg = TweetGetter(TornadoApp.ckey,
                             TornadoApp.csecret, 
                             TornadoApp.atoken,
                             TornadoApp.asecret)
            print (json_message)
            tweet_num = int(json_message["tweet_num"])
            result = bandit_client.select_arm(tweet_num)
            user_set = set([x[1] for x in result])
            ignore_user = []
            tweets_dict = {}
            for user in user_set:
                print ("get tweet of {}".format(user))
                tweets_dict[user] = tg.get_tweet(user, tweet_num)
                if tweets_dict[user] == None:
                    ignore_user.append(user)

            result_dict = {}
            result_dict["type"] = "select"
            result_dict["data"] = {}
            
            for i, elem in enumerate(result):
                user = elem[1]
                if user in ignore_user:
                    continue
                tweet_data = tweets_dict[user].pop(0)
                text = tweet_data["text"]
                user_url = "https://twitter.com/{}".format(user)
                img_src = tweet_data["user"]["profile_image_url"]
                result_dict["data"][i] = {"category": elem[0], "user": elem[1], "text":text, "img_src": img_src, "user_url": user_url}
            
            self.write_message((json.dumps(result_dict)))

        elif message_type == "update":
            userid = json_message["user"]
            if userid == "":
                self.write_message(json.dumps({"type": "none", "msg": "this arm is already rewarded"}))
            else:
                category = json_message["category"]
                bandit_client.register_reward(category, userid)
                arm_info = bandit_client.get_arm_info("global")
                print ("update {} arm in category server".format(category))
                print (arm_info["category"])
                print ("update {} arm in {} server".format(userid, category))
                print (arm_info[category])
                self.write_message(json.dumps({"type":"update", "user":userid, "category":category}))

    def on_close(self):
        print("web socket closed")


class TornadoApp():
    category_port = 0
    categories = []
    ports = []
    bandit_client = None
    json_config = None
    ckey = ""
    csecret = ""
    atoken = ""
    asecret = ""
    base_dir = os.path.dirname(__file__)
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/ws", BanditHandler)
    ], 
    template_path = os.path.join(base_dir, "..", "..", "templates"),
    static_path = os.path.join(base_dir, "..", "..", "static")
    )
    server = httpserver.HTTPServer(app)
    def initialize(self, json_config, access_token):
        TornadoApp.category_port = int(json_config["port"])
        TornadoApp.categories = list(json_config["category"].keys())
        TornadoApp.ports = [int(json_config["category"][c]["port"]) for c in json_config["category"]]
        TornadoApp.json_config = json_config
        TornadoApp.ckey = access_token["ck"]
        TornadoApp.csecret = access_token["cs"]
        TornadoApp.atoken = access_token["at"]
        TornadoApp.asecret = access_token["as"]

if __name__ == '__main__':
    with open(sys.argv[1]) as conf:
        with open(sys.argv[2]) as token:
            json_config = json.load(conf)
            access_token = json.load(token)
            t = TornadoApp()
            t.initialize(json_config, access_token)
    port = 9000
    print("start tornado server listening at {}".format(port))
    t.app.listen(port)
    tornado.ioloop.IOLoop.instance().start()
