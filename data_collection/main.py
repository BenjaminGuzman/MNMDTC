# -*- coding: utf-8 -*-

from twython import Twython
import re
import json
import os
import getopt
import sys
import datetime
import pandas as pd

from web_scraping import get_tweet, am_i_using_tor
from bcolors import bcolors

URL_COMPLETE_TWEET_REGEX = re.compile(r"… https://t\.co/(.*)+$")
TODAY = datetime.datetime.today()

def twython_authenticate():
    twitter = None
    with open("./config.json", 'r') as config_file:
        config = json.load(config_file)
        config_SRMDTC = config["apikeys"]["SRMDTC"]
        twitter = Twython(config_SRMDTC["app_key"], config_SRMDTC["app_secret"], config_SRMDTC["oauth_token"],
                          config_SRMDTC["oauth_token_secret"])
        twitter.verify_credentials()

    return twitter


def get_last_tweet_id(last_file):
    print("Retrieving last ID from {}".format(last_file))
    regex_replace_chars = re.compile(r"[#@áéíóúäëïöüÁÉÍÓÚñÑ]+", re.IGNORECASE)
    sanitized_file_name = re.sub(regex_replace_chars, '_', last_file)
    df = pd.read_json("out/{}".format(sanitized_file_name), lines=True)
    max_id = df["id"].max()
    print("Last ID: {}".format(max_id))
    return max_id



def check_dirs():
    out = "./out"
    out_complete = "./out_complete"

    if not os.path.isdir(out):
        os.mkdir(out)

    if not os.path.isdir(out_complete):
        os.mkdir(out_complete)


def get_paths_and_geocode(query, latitude, longitude, radius):
    regex_replace_chars = re.compile(r"[#@áéíóúäëïöüÁÉÍÓÚñÑ]+", re.IGNORECASE)
    sanitized_file_name = re.sub(regex_replace_chars, '_', query)
    file_path = "./out/{}.json".format(sanitized_file_name)
    file_path_complete = "./out_complete/{}.json".format(sanitized_file_name)

    geocode = "{},{},{}".format(latitude, longitude, radius)

    return file_path, file_path_complete, geocode


def get_url_to_complete_tweet(text):
    result_search = re.search(URL_COMPLETE_TWEET_REGEX, text)
    # [2:] : remove "… "
    return result_search.group(0)[2:]


class Main:
    def __init__(self):
        self.twitter = twython_authenticate()

    def search_and_save(self, q, count=1000, latitude="19.42", longitude="-99.12", radius="10km", result_type="recent", include_entities=True, since_id=0):
        file_path, file_path_complete, geocode = get_paths_and_geocode(q, latitude, longitude, radius)

        check_dirs()

        print("Retrieving tweets for: \"{}\"...".format(q))
        tweets = self.twitter.search(q=q, count=count, geocode=geocode, result_type=result_type, include_entities=include_entities, since_id=since_id)

        print("Retrieving complete tweets...")

        tweets_for_pandas = ''
        i = 0
        for tweet in tweets["statuses"]:
            i += 1
            if tweet["truncated"] is True:
                url_to_complete_tweet = get_url_to_complete_tweet(tweet["text"])
                tweet["text"] = get_tweet(url_to_complete_tweet)
                tweet["url"] = url_to_complete_tweet
            tweets_for_pandas += "{}\r\n".format(json.dumps(tweet))

        print("# tweets: {}\r\n".format(i))

        with open(file_path, 'a') as file:
            file.write(tweets_for_pandas)

        with open(file_path_complete, 'a') as file:
            file.write(json.dumps(tweets))

        return


def main(keyword_list="./delinquency.list", keyword_=False, since_id_=0, previous_=False):
    print("Starting...")

    main_obj = Main()

    keywords = []
    # load keywords from file
    if keyword_ is False:
        with open(keyword_list, 'r') as list:
            keywords = [line.strip('\n') for line in list]
    else:
        keywords = [keyword_]

    if previous_ is True:
        for curr_keyword in keywords:
            main_obj.search_and_save(
                curr_keyword,
                radius="50km",
                since_id=get_last_tweet_id("{}.json".format(curr_keyword))
            )
    else:
        for curr_keyword in keywords:
            main_obj.search_and_save(curr_keyword, radius="50km", since_id=since_id_)

    print("Done")


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:k:f:p", ["list=", "keyword=", "last-file=", "previous"])
    except:
        print("Usage: ")
        print("{}-l{} | {}--list{}: file that contains the keywords to search".format(bcolors.BOLD, bcolors.ENDC, bcolors.BOLD, bcolors.ENDC))
        print("{}-k{} | {}--keyword{}: single keyword to search".format(bcolors.BOLD, bcolors.ENDC, bcolors.BOLD, bcolors.ENDC))
        print("{}-f{} | {}--last-file{}: get the greater tweet ID in the given file and search tweets greater that the ID".format(bcolors.BOLD, bcolors.ENDC, bcolors.BOLD, bcolors.ENDC))
        print("{}-p{} | {}--previous{}: Needs --list parameter, and search for all tweets starting from the last id (inside out/[keyword].json)".format(bcolors.BOLD, bcolors.ENDC, bcolors.BOLD, bcolors.ENDC))
        print("Obviously list and keyword parameters cannot be combined")
        sys.exit(2)

    list = False
    keyword = False
    last_file = False
    previous = False
    since_id = 0

    if am_i_using_tor() is True:
        print("{}YOU'RE USING TOR!!!{}".format(bcolors.WARNING, bcolors.ENDC))
        user_input = input("Continue? (n|N to quit)\r\n")
        if user_input == "N" or user_input == "n":
            sys.exit(0)
    else:
        print("{}YOU'RE NOT USING TOR{}".format(bcolors.OKGREEN, bcolors.ENDC))

    if len(opts) == 0:
        main()
        sys.exit(0)

    opt, arg = opts[0]

    if opt in ("-l", "--list"):
        list = arg
    elif opt in ("-f", "--last-file"):
        last_file = arg
        last_retrieved_tweet_id = get_last_tweet_id(last_file)
        keyword = last_file.replace(".json", '')
        list = None
        since_id = last_retrieved_tweet_id
    elif opt in ("-p", "--previous"):
        previous = True
        opt, arg = opts[1]
        list = arg
    elif opt in ("-k", "--keyword"):
        keyword = arg

    main(list, keyword, since_id, previous)
