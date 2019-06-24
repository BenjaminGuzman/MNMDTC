import requests
from bs4 import BeautifulSoup
import getopt
import sys
import os
from ast import literal_eval

session = requests.session()

# TODO: REMOVE THIS, CAREFUL WITH THIS
# TODO: Quitar esto, en el tec no usar TOR
USING_TOR = True

if USING_TOR is True:
    session.proxies = {
        "http": "socks5h://localhost:9050",
        "https:": "socks5h://localhost:9050",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    }


def am_i_using_tor():
    tor_ip = session.get("http://httpbin.org/ip")
    real_ip = requests.get("http://httpbin.org/ip")

    tor_ip_dict = literal_eval(tor_ip.text)
    real_ip_dict = literal_eval(real_ip.text)

    print("Real IP: {}".format(real_ip_dict["origin"]))
    print("TOR IP: {}".format(tor_ip_dict["origin"]))

    return tor_ip_dict["origin"] != real_ip_dict["origin"]


def get_tweet(url):

    html_soup = _request_tweet(url)
    return _get_tweet_from_html(html_soup)


def _request_tweet(url):
    status = "OK"
    return_soap = None

    html = session.get(url)

    if html.status_code != 200:
        status = "NOT OK!!!"
    else:
        return_soap = BeautifulSoup(html.text, "html.parser")

    print("{}: {}".format(url, status))
    return return_soap


def _get_tweet_from_html(soup):
    text_container = soup.select(".js-original-tweet .js-tweet-text.tweet-text")
    text_content = text_container[0].text

    return text_content


# class bcolors from https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:", ["url="])
    except:
        print("Usage: {}-u{} | {}--url{}: file that contains the keywords to search".format(bcolors.BOLD, bcolors.ENDC, bcolors.BOLD, bcolors.ENDC))
        sys.exit(2)

    opt, url_arg = opts[0]

    print(get_tweet(url_arg))
