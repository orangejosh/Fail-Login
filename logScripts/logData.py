import sys
import sqlite3
from sqlite3 import Error
import urllib, json
import re

args = sys.argv

def main():
	# Assumes a database has ben created
    conn = create_connection("/home/pi/logData/logData.db")
    create_all_tables(conn)

    with conn:
        f = open(args[1])
        for i in f:
            str = re.split('"', i)

            try:
                city = str[1].decode('utf-8')
                region = str[3].decode('utf-8')
                country = str[5].decode('utf-8')
            except:
                city = ""
                region = ""
                country = ""

            str = i.split()

            month = str[0].decode('utf-8')
            day = str[1].decode('utf-8')
            time = str[2].decode('utf-8')

            user = str[3].decode('utf-8')
            ip = str[4].decode('utf-8')

            date = (month, day)
            sql = ''' INSERT OR IGNORE INTO dates(month, day) VALUES(?,?) '''
            create_row(conn, sql, date)
            sql = ''' SELECT id FROM dates WHERE month=? AND day=? '''
            date_id = get_row_id(conn, sql, date)

            username = (user,)
            sql = ''' INSERT OR IGNORE INTO users(username) VALUES(?) '''
            create_row(conn, sql, username)
            sql = ''' SELECT id FROM users WHERE username=? '''
            user_id = get_row_id(conn, sql, username)

            location = (city, region, country)
            sql = ''' INSERT OR IGNORE INTO locations(city, region, country) VALUES(?,?,?) '''
            create_row(conn, sql, location)
            sql = ''' SELECT id FROM locations WHERE city=? AND region=? AND country=? '''
            location_id = get_row_id(conn, sql, location)

            log = (time, ip, user_id, date_id, location_id) 
            sql = ''' INSERT INTO logs(time, ip, user_id, date_id, location_id) VALUES (?,?,?,?,?) '''
            log_id = create_row(conn, sql, log)
#            x += 1


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None

def create_all_tables(conn):
    date_table = """CREATE TABLE IF NOT EXISTS dates (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        month TEXT,
                        day INTEGER,
                        UNIQUE(month, day)
                    );"""

    location_table = """CREATE TABLE IF NOT EXISTS locations (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        city TEXT,
                        region TEXT,
                        country TEXT,
                        UNIQUE(city, region, country)
                    );"""

    user_table = """CREATE TABLE IF NOT EXISTS users (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        UNIQUE(username)
                    );"""

    log_table = """CREATE TABLE IF NOT EXISTS logs (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        time TEXT NOT NULL,
                        ip TEXT NOT NULL,
                        user_id, INTEGER,
                        date_id INTEGER,
                        location_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (date_id) REFERENCES dates (id),
                        FOREIGN KEY (location_id) REFERENCES locations (id)
                    );"""

    if conn is not None:
        create_table(conn, date_table)
        create_table(conn, location_table)
        create_table(conn, user_table)
        create_table(conn, log_table)
    else:
        print("Error: cannot create database connection")

def create_table(conn, table):
    try:
        c = conn.cursor()
        c.execute(table)
    except Error as e:
        print(e)

def create_row(conn, sql, obj):
    cur = conn.cursor()
    cur.execute(sql, obj)

def get_row_id(conn, sql, obj):
    cur = conn.cursor()
    cur.execute(sql, obj)
    return cur.fetchall()[0][0]

main()
