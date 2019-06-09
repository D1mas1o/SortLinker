import sqlite3
import requests
import random
import string

def get_short_url(data):
    if data.form['user_url'] is not None and data.form['LinkMode'] is not None:
        try:
            requests.get(data.form['user_url'])
            short_link = get_hash()
            long_link =data.form['user_url']
            link_mode = data.form['LinkMode']
            with sqlite3.connect('ShortLinkBd.db') as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Links (LongLink,ShortLink,LinkMode) VALUES (?,?,?)',(long_link,short_link,link_mode))
            return "http://127.0.0.1:5000/sh.ly/" + short_link
        except requests.exceptions.MissingSchema:
            return "Введите корретную ссылку"


def get_hash():
    while True:
        hash = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=random.randint(8,12)))
        with sqlite3.connect('ShortLinkBd.db') as conn:
            c = conn.cursor()
            c.execute('SELECT ShortLink From Links Where ShortLink = (?) ',(hash,))
            list = c.fetchall()
        if len(list) == 0:
            return hash

def short_answer(short_url):
    with sqlite3.connect('ShortLinkBd.db') as conn:
        c = conn.cursor()
        c.execute('SELECT LongLink,LinkMode FROM Links WHERE ShortLink=(?)',(short_url,))

        mas = c.fetchone()
        long_link = mas[0]
        link_mode = mas[1]
    return long_link,link_mode

def check_auth(username, password):
    try:
        with sqlite3.connect('ShortLinkBd.db') as conn:
            c = conn.cursor()
            c.execute('SELECT Password FROM Users WHERE Login=(?)', (username,))
            qwer = c.fetchone()[0]
            return username == username and password == qwer
    except TypeError:
        return False
