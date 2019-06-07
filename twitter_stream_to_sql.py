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

def data_extract(json_):
    """
    Extracts data from every tweet
    """
    msg_id = json_["id"]
    msg_users_id = json_["user"]["id"]
    msg_timestamp = json_["timestamp_ms"]
    if "RT @" in json_["text"]:
        if json_["retweeted_status"]["truncated"]:
            msg_text = json_["retweeted_status"]["extended_tweet"]["full_text"]
        else:
            msg_text = json_["retweeted_status"]["text"]
    else:
        if json_["truncated"]:
            msg_text = json_["extended_tweet"]["full_text"]
        else:
            msg_text = json_["text"]
    
    users_name = json_["user"]["screen_name"]
    users_id = msg_users_id
    users_desc = json_["user"]["description"]
    users_follows = json_["user"]["friends_count"]
    users_followers = json_["user"]["followers_count"]
    user_tweets = json_["user"]["statuses_count"]

    return (str(msg_id), str(msg_users_id), str(msg_timestamp), str(msg_text), 
    str(users_name), str(users_id), str(users_desc), users_follows, users_followers, user_tweets)



class MyListener(StreamListener):
    
    def on_connect(self):
        print("Conected!")
        
    def on_status(self, data):
        
        try:            
            print(data_extract(data._json))
            
            txt_SQL = data_extract(data._json)
                
#            stringTextoParaSql = json['text'].replace("\'", "\"").replace("\n", " ")
#            textoEnSql = "INSERT INTO Mensaje (Texto, Usuario, Enlace) VALUES (REPLACE(REPLACE(REPLACE('"+stringTextoParaSql+"', '!', ''), '#', ''), '$', ''), " + str(json['user']['id']) +", NULL)"
            cursor.execute("INSERT INTO dbo.msg VALUES ('{}', '{}', '{}', '{}')".format(txt_SQL[0], txt_SQL[1], txt_SQL[2], txt_SQL[3]))
            cursor.execute("INSERT INTO dbo.users VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(txt_SQL[4], txt_SQL[5], txt_SQL[6], txt_SQL[7],txt_SQL[8], txt_SQL[9] ))

            print(txt_SQL[3])
            print()
            return True

        except Exception as e:
            print("Error onjson: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print("ERROR!")
        print(status)
        return True


if __name__ == '__main__':
    auth = OAuthHandler(configLocal.consumer_key, configLocal.consumer_secret)
    auth.set_access_token(configLocal.access_token, configLocal.access_secret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(
        locations = configLocal.coordenadas, 
#        track= [queryParaTwitter], 
        languages=['es']
    )