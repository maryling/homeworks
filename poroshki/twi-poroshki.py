# 1) скачать из ВК все посты, которые состоят из 5 строк
# 2) сделать БД с постами и их id
# 3) раз в день повторять процедуру выкачивания, начиная с последнего
# 4) постить случайный порошок раз в три часа
# 5) захостить на сервере

import tweepy
import time 
from credentials import *
import urllib.request
import json
import sqlite3
import re


def get_texts():
    offsets = [0, 100, 200, 300, 400, 500]
    texts = {}
    for off in offsets:
        req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-31481258&count=100&v=5.74&'
                                     'access_token=b6115d00b6115d00b6115d0015b673718fbb611b6115d00ecd0bed6fb1fbee7bdd1987a&offset=' + str(off))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        print(data)
        for i in range(len(data["response"]["items"])):
            texts[data["response"]["items"][i]["id"]] = data["response"]["items"][i]["text"]
    return texts


def posts_to_db():
    texts = get_texts()
    poroshok = re.compile(r'(.*?)\n(.*?)\n(.*?)\n(.*?)', flags=re.DOTALL)
    conn = sqlite3.connect('poroshki.db')
    c = conn.cursor()
    c.execute("CREATE TABLE posts(post_id, text)")
    for p_id in texts:
        text = texts[p_id]
        if poroshok.match(text):
            c.execute("INSERT INTO posts VALUES(?, ?)", (p_id, text))
    conn.commit()
    conn.close()
    return "ok"


def update_db():
    conn = sqlite3.connect('poroshki.db')
    c = conn.cursor()
    ids = c.execute("SELECT id FROM posts").fetchall()
    last_id = max(ids)
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-31481258&count=100&v=5.74&'
                                 'access_token=b6115d00b6115d00b6115d0015b673718fbb611b6115d00ecd0bed6fb1fbee7bdd1987a')
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    texts = {}
    poroshok = re.compile(r'(.*?)\n(.*?)\n(.*?)\n(.*?)', flags=re.DOTALL)
    for i in range(len(data["response"]["items"])):
        if data["response"]["items"][i]["id"] > last_id:
            texts[data["response"]["items"][i]["id"]] = data["response"]["items"][i]["text"]
            for p_id in texts:
                text = texts[p_id]
                if poroshok.match(text):
                    c.execute("INSERT INTO posts VALUES(?, ?)", (p_id, text))
            conn.commit()
            conn.close()


def post_poroshki():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    conn = sqlite3.connect('poroshki.db')
    c = conn.cursor()
    poroshki = c.execute("SELECT text FROM posts").fetchall()
    for poroshok in poroshki:
        api.update_status(poroshok[0])
        time.sleep(10800)


def main():
    # posts_to_db()
    old_time = time.time()
    if time.time() - old_time > 86399:
        update_db()
        print("db updated")
    post_poroshki()


if __name__ == "__main__":
    main()
