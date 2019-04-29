import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import string
import config
import pyodbc 
import configLocal
import json
import datetime
from time import gmtime, strftime
from pathlib import Path
import os

separador = '¿¡@(,'
directorioArchivo = configLocal.directorioArchivo
queryParaTwitter = configLocal.query



server = configLocal.server
database = configLocal.database
username = configLocal.username
password = configLocal.password
cnxn = configLocal.cnxn
cursor = cnxn.cursor()

def data_extract(json):
    """
    Extracts data from every tweet
    """
    msg_id = json["id"]
    msg_users_id = json["user"]["id"]
    msg_timestamp = json["created_at"]
    if "RT @" in json["text"]:
        if json["retweeted_status"]["truncated"]:
            msg_text = json["retweeted_status"]["extended_tweet"]["full_text"]
        else:
            msg_text = json["retweeted_status"]["text"]
    else:
        if json["truncated"]:
            msg_text = json["extended_tweet"]["full_text"]
        else:
            msg_text = json["text"]
    
    users_name = json["user"]["screen_name"]
    users_id = msg_users_id
    users_desc = json["user"]["description"]
    users_follows = json["user"]["friends_count"]
    users_followers = json["user"]["followers_count"]
    user_tweets = json["user"]["statuses_count"]

    return (str(msg_id), str(msg_users_id), msg_timestamp, msg_text, 
    users_name, users_id, users_desc, users_follows, users_followers, user_tweets)



class MyListener(StreamListener):
    def on_connect(self):
        print("Conected!")
    def on_status(self, data):
        
        try:
            json = data_extract(json.loads(data))
            txt_SQL = data_extract(json)
                
#            stringTextoParaSql = json['text'].replace("\'", "\"").replace("\n", " ")
#            textoEnSql = "INSERT INTO Mensaje (Texto, Usuario, Enlace) VALUES (REPLACE(REPLACE(REPLACE('"+stringTextoParaSql+"', '!', ''), '#', ''), '$', ''), " + str(json['user']['id']) +", NULL)"
            cursor.execute('INSERT INTO dbo.msg VALUES ({}, {}, {}, N {}'.format(txt_SQL[0], txt_SQL[1], txt_SQL[2], txt_SQL[3]))
            cursor.execute('INSERT INTO dbo.users VALUES (N {}, N {}, N {}, {}, {}, {}'.format(txt_SQL[4], txt_SQL[5], txt_SQL[6], txt_SQL[7],txt_SQL[8], txt_SQL[9] ))

            print(json['text'])

            return True

        except BaseException as e:
            print("Error onjson: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == '__main__':
    auth = OAuthHandler(configLocal.consumer_key, configLocal.consumer_secret)
    auth.set_access_token(configLocal.access_token, configLocal.access_secret)
    api = tweepy.API(auth)

twitter_stream = Stream(auth, MyListener(directorioArchivo, queryParaTwitter))
twitter_stream.filter(locations = configLocal.coordenadas, track= [queryParaTwitter], languages=['es'])
