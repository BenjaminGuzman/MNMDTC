# -*- coding: utf-8 -*-

from twython import Twython
import re
import json
import os



def twython_authenticate():
    twitter = None
    with open("./config.json", 'r') as config_file:
        config = json.load(config_file)
        config_SRMDTC = config["apikeys"]["SRMDTC"]
        twitter = Twython(config_SRMDTC["app_key"], config_SRMDTC["app_secret"], config_SRMDTC["oauth_token"],
                          config_SRMDTC["oauth_token_secret"])
        twitter.verify_credentials()

    return twitter


def main():
    twitter = twython_authenticate()
    print("Tráfico 88.9 ID: {}".format(twitter.lookup_user(screen_name="trafico889")[0]["id"]))




if __name__ == '__main__':
    main()
