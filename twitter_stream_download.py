import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import pyodbc 
import configLocal
import json
import datetime
from time import gmtime, strftime
from pathlib import Path
import os

separador = 'ef5r64i'
directorioArchivo = configLocal.directorioArchivo
queryParaTwitter = 'e'



server = configLocal.server
database = configLocal.database
username = configLocal.username
password = configLocal.password
cnxn = configLocal.cnxn
cursor = cnxn.cursor()


barcelona = [2.090903, 41.335847, 2.220298, 41.461651] #Venid a verla, es una ciudad muy bonita!

def get_parser():
    """Get parser for command line arguments."""

    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.outfile = "%s/stream_%s.csv" % (data_dir, query_fname)

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            with open(self.outfile, 'a') as f:
                #Para meterlo en la base de datos
                if "RT @" in json_data["text"]:
                    if json_data["retweeted_status"]["truncated"]:
                        stringTextoParaSql = json_data["retweeted_status"]["extended_tweet"]["full_text"]
                        #stringUrls = json_data["retweeted_status"]["entities"]["urls"][0]['display_url'] if len(json_data["retweeted_status"]["entities"]["urls"]) > 0 else ""
                    else:
                        stringTextoParaSql = json_data["retweeted_status"]["text"]
                        #stringUrls = json_data["retweeted_status"]['entities']['urls'][0]['display_url'] if len(json_data["retweeted_status"]['entities']['urls']) > 0 else ""
                else:
                    if json_data["truncated"]:
                        stringTextoParaSql = json_data["extended_tweet"]["full_text"]
                        #stringUrls = json_data["extended_entities"]['media'][0]['display_url'] if len(json_data["extended_entities"]['media']) > 0 else ""
                    else:
                        stringTextoParaSql = json_data["text"]
                        #stringUrls = json_data['entities']['urls']
                stringTextoParaSql = stringTextoParaSql.replace("\'", "\"").replace("\n", " ")
                # textoEnSql = "INSERT INTO Mensaje (IdTweet, NombreUsuario, IdUsuario, ) VALUES (REPLACE(REPLACE(REPLACE('"+stringTextoParaSql+"', '!', ''), '#', ''), '$', ''), " + str(json_data['user']['id']) +", NULL)"
                # cursor.execute(textoEnSql)

                print(stringTextoParaSql)

                #Para guardarlo en .csv
                string_para_guardar = '\n' + stringTextoParaSql + separador\
                + str(json_data['user']['id']) + separador\
                + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + separador\
                + str(json_data["id"]) + separador\
                + json_data["user"]["screen_name"] + separador\
                + str(json_data["created_at"]) + separador\
                + ' '.join([a['text'] for a in json_data['entities']['hashtags']]) + separador\
                + ""#stringUrls#json_data['entities']['urls'][0]['url'] if len(json_data['entities']['urls']) > 0 else ""
                f.write(string_para_guardar)

                return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    args.data_dir = directorioArchivo
    args.query = queryParaTwitter
    print('args', args)
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    exists = os.path.isfile("%s/stream_%s.csv" % (args.data_dir, format_filename(args.query)))
    if not exists:
        with open("%s/stream_%s.csv" % (args.data_dir, format_filename(args.query)), 'a') as f:
            f.write('Texto'+ separador+'IdUsuario'+ separador +'FechaCreacion'+separador+'IdTweet'+separador+'NombreUsuario'+separador+
            'FechaCreacionTweet'+separador+'Hashtags'+separador+'Url')
        

#Para crear el fichero
    # with open("%s/stream_%s.csv" % (args.data_dir, format_filename(args.query)), 'a') as f:
    #     f.write('Texto'+ separador+'IdUsuario'+ separador +'FechaCreacion'+separador+'IdTweet'+separador+'NombreUsuario'+separador+
    #     'FechaCreacionTweet'+separador+'Hashtags'+separador+'Url')

twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
#twitter_stream.filter(locations=barcelona)
twitter_stream.filter(locations = barcelona, track= [args.query], languages=['es'])
#twitter_stream.filter(locations = barcelona, track= [args.query])