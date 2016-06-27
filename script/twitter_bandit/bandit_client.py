# -*- coding:utf-8 -*-

import jubatus

class TwitterBanditClient():
    def __init__(self, 
                 category_port,
                 categories, 
                 ports,
                 category_name = "category"):
        self.category_name = category_name
        self.client = {}
        self.categories = categories
        self.client[self.category_name] = jubatus.Bandit("localhost", category_port, category_name, 0)
        for name, port in zip(categories, ports):
            self.client[name] = jubatus.Bandit("localhost", port, name, 0)

    def initialize_arms(self, json_config):
        print(self.client)
        cl = self.client[self.category_name]
        for category in json_config[self.category_name]:
            cl.register_arm(category)
            cl_category = self.client[category]
            for user in json_config[self.category_name][category]["user"]:
                if cl_category.register_arm(user):
                    print("{}".format(user))
                else:
                    print("failed {}".format(user))

    def select_arm(self, tweet_num = 10):
        result = [""] * tweet_num
        for i in range(tweet_num):
            selected_category = self.client[self.category_name].select_arm("global")
            selected_user = self.client[selected_category].select_arm("global")
            result[i] = (selected_category, selected_user)
        return result
    
    def register_reward(self, category, user):
        self.client["category"].register_reward("global", category, 1.0)
        self.client[category].register_reward("global", user, 1.0)

    def get_arm_info(self, player):
        result_dict = {}
        for cl in self.client:
            result_dict[cl] = self.client[cl].get_arm_info(player)
        return result_dict

    def reset_arm(self):
        for cl in self.client:
            self.client[cl].reset("global")

    def save(self):
        for cl in self.client:
            self.client[cl].save(cl)

