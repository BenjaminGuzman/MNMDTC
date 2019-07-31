# -*- coding: utf-8 -*-

from twython import TwythonStreamer
import json
import os
import re
import pandas as pd
import pipes




class Streamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
         print(data['text'])

             
            
        

def on_error(self, status_code, data):
  print(status_code, data)



def main():
    with open("./config.json", 'r') as config_file:
        config = json.load(config_file)
        config_SRMDTC = config["apikeys"]["MNMDTC"]
        stream = Streamer(config_SRMDTC["app_key"], config_SRMDTC["app_secret"], config_SRMDTC["oauth_token"],
                          config_SRMDTC["oauth_token_secret"])
    stream.statuses.filter(follow=40098528)









if __name__ == '__main__':
    main()



