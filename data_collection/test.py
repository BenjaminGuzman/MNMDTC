from TwitterAPI import TwitterAPI
import json

with open("./config.json", 'r') as config_file:
    config = json.load(config_file)
config_SRMDTC = config["apikeys"]["SRMDTC"]

api = TwitterAPI(config_SRMDTC["app_key"], config_SRMDTC["app_secret"], config_SRMDTC["oauth_token"], config_SRMDTC["oauth_token_secret"])

r = api.request('statuses/filter', {'locations': '19,425,-99,125'})
for item in r:
    print(item)