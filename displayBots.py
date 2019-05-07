#############################################################################
# displayBots.py
#   arugemnts: path/to/database
#              Min number of bots in botnet to display attack (optional)
#   
# Description:
#   Loops through each entry in the bots table. Displays the month, day
#   time, username, ip, city, region, country, number of bots in botnet, and bot_id.
#   It groups each login attempt with attempts that are probably from the same bot.
# 
#############################################################################


import sys
import sqlite3
from sqlite3 import Error

count = 0

def main():
    if len(sys.argv) == 3:
        count = sys.argv[2]
    elif len(sys.argv) == 1 or len(sys.argv) > 3:
        print "Argument Error, format arguments like:"
        print "     python displayBots.py /path/to/database count(optional)"
        print "     count is the min. number of bots in botnet to display"
        return

    conn = create_connection(sys.argv[1])
    with conn:
        sql = ''' SELECT id FROM bots '''
        attacks = get_rows(conn, sql)
        print_attacks(conn, attacks)

# Connect to database
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None

# Get all the attack id's
def get_rows(conn, sql):
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()

def print_attacks(conn, attacks):
    for bot_net in attacks:
        bot_id = (bot_net[0], count)
        sql = ''' SELECT month, day, time, username, ip, city, region, country, count, bot_id FROM logs
                    JOIN dates ON logs.date_id = dates.id
                    JOIN users ON logs.user_id = users.id
                    JOIN locations ON logs.location_id = locations.id 
                    JOIN bots ON logs.bot_id = bots.id
                    WHERE logs.bot_id = ? AND bots.count >= ? '''

        cur = conn.cursor()
        cur.execute(sql, bot_id)
        bot = cur.fetchall()

        if len(bot) > 0:
            print_bot(conn, bot)

def print_bot(conn, bots):
    for bot in bots:
        print(bot)

    print(" ")


main()
