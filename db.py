import sqlite3
from datetime import datetime
from util import date_to_str

# TODO change this to actual 1970 EPOCH just for aesthetics
EPOCH = 1697070014

conn = sqlite3.connect('twistr.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    handle TEXT NOT NULL,
    last_tweet_date TEXT NOT NULL,
    last_download_date TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS system (
    id INTEGER PRIMARY KEY,
    last_login_date TEXT NOT NULL,
    last_download_date TEXT NOT NULL
)
''')

if len(cursor.execute('SELECT * FROM system').fetchall()) == 0:
    cursor.execute("INSERT INTO system (id, last_login_date, last_download_date) VALUES (1, ?, ?)", (date_to_str(datetime.fromtimestamp(EPOCH)), date_to_str(datetime.fromtimestamp(EPOCH))))
    conn.commit()

def get_user_id(handle):
    user_id = cursor.execute('SELECT user_id FROM users WHERE handle = ?', (handle,)).fetchone()

    if user_id is None:
        return None
    else:
        return user_id[0]

def get_user_last_tweet_date(user_id):
    return cursor.execute('SELECT last_tweet_date FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]


def insert_user(user_id, handle, last_tweet_date = date_to_str(datetime.fromtimestamp(EPOCH)), last_download_date = date_to_str(datetime.fromtimestamp(EPOCH))):
    cursor.execute('INSERT INTO users (user_id, handle, last_tweet_date, last_download_date) VALUES (?, ?, ?, ?)', (user_id,handle,last_tweet_date,last_download_date))
    conn.commit()

def update_user(user_id, last_tweet_date, last_download_date):
    cursor.execute('UPDATE users SET last_tweet_date = ?, last_download_date = ? WHERE user_id = ?', (last_tweet_date,last_download_date, user_id))
    conn.commit()

def update_system(last_login_date = None, last_download_date = None):
    query = 'UPDATE system SET '
    params = ()

    if last_login_date:
        query += 'last_login_date = ? '
        params += (last_login_date,)
    elif last_download_date:
        if len(params) > 0:
            query += (', ',)

        query += 'last_download_date = ? '
        params += (last_download_date,)
    else:
        return


    cursor.execute(query, params)
    conn.commit()

def get_system_dates():
    return cursor.execute('SELECT last_login_date, last_download_date FROM system').fetchone()
