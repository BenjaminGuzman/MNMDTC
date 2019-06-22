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

class Main:
    def __init__(self):
        self.twitter = twython_authenticate()

    def search_and_save(self, q, count=1000, latitude="19.4284700", longitude="-99.1276600", radius="20km", result_type="recent", include_entities=True):
        regex_replace_chars = re.compile(r"[#@áéíóúäëïöüÁÉÍÓÚñÑ]+", re.IGNORECASE)
        file_name = "./out/{}.json".format(re.sub(regex_replace_chars, '_', q))

        geocode = "{},{},{}".format(latitude, longitude, radius)

        if not os.path.isdir("./out"):
            os.mkdir("./out")

        print("Saving file...")
        with open(file_name, 'a') as file:
            file.write(str.format("{}\r\n", self.twitter.search(q=q, count=count, geocode=geocode, result_type=result_type, include_entities=include_entities)))
        return


def main():
    print("Starting...")

    main_obj = Main()
    main_obj.search_and_save("#delincuencia", 100)

    print("Done")


if __name__ == '__main__':
    main()
