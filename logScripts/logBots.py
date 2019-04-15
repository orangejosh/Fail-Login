#############################################################################
# logBots.py
#   arugemnts: path/to/database
#   globals: MAX_BOT_TIME - The max time between login attemps to be
#    considered related.
#   
# Description:
#   Checks every entry in the log database against the next entry.
#   If both entries meet certain criteria they are considered most
#   likely from the same source. Each group is logged into a single
#   row of the table bots. The row has an id, a start time, an
#   end time, and a count of how many entries it has. The log entries
#   are then updated as to the bot its attached to.
# 
#############################################################################

import sys
import sqlite3
from sqlite3 import Error

DATABASE = sys.argv[1] 
MAX_BOT_TIME = 3


def main():
    conn = create_connection(DATABASE)

    with conn:
        cur = conn.cursor()

        # Every attempted login entry in the log
        sql = ''' SELECT date_id, time, username FROM logs
                    JOIN dates ON logs.date_id = dates.id
                    JOIN users ON logs.user_id = users.id '''
        cur.execute(sql)

        bot_id = None
        row = next(cur, None)
        
        while row is not None:
            next_row = next(cur, None)
            if next_row is None:
                break

            # Tests if this row and next_row meet the criteria for a bot            
            # date_id, and username must match. Must be close in time
            if row[0] == next_row[0] and \
               row[2] == next_row[2] and \
               close_in_time(row[1], next_row[1]):
                if bot_id is None:
                    bot_id = create_bot(conn, bot_id, row, next_row)
                else:
                    update_bot(conn, bot_id, next_row)
            else:
                bot_id = None

            row = next_row


# Connect to database
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None

# Returns true if the two times are within MAX_BOT_TIME minutes of each other
def close_in_time(time, next_time):
    time_list = time.split(":")

    hour = int(time_list[0])
    minute = int(time_list[1])

    next_time_list = next_time.split(":")

    next_hour = int(next_time_list[0])
    next_minute = int(next_time_list[1])

    if hour == next_hour and next_minute - minute < MAX_BOT_TIME:
        return True
    elif next_hour - 1 == hour and next_minute + (60 - minute) < MAX_BOT_TIME:
        return True
    else:
        return False


# Create a bot entry in the database with id, start time, end_time, and count
def create_bot(conn, bot_id, row, next_row):
    cur = conn.cursor()

    date_id = row[0]
    next_date_id = next_row[0]

    time = row[1]
    next_time = next_row[1]

    # Is duplicate?
    bot = (date_id, time) 
    sql = ''' SELECT id FROM bots WHERE date_id = ? AND start_time = ? '''
    cur.execute(sql, bot)
    duplicate = len(cur.fetchall()) > 0 

    if not duplicate:
        # Create the new row and return its id
        bot = (date_id, time, next_time, 2)
        sql = ''' INSERT OR IGNORE INTO bots (date_id, start_time, end_time, count) VALUES (?, ?, ?, ?) '''
        cur.execute(sql, bot)
        bot_id = cur.lastrowid

        # Update the logs with the id of the bot attack
        sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''

        bot = (bot_id, date_id, time)
        cur.execute(sql, bot)

        bot = (bot_id, next_date_id, next_time)
        cur.execute(sql, bot)

    return bot_id


# Update the bot's end_time
def update_bot(conn, bot_id, next_row):
    if bot_id is not None:
        cur = conn.cursor()

        next_date_id = next_row[0]
        next_time = next_row[1]

        # Update end_time of bot
        bot = (next_time, bot_id)
        sql = ''' UPDATE bots SET end_time = ? WHERE id = ? '''
        cur.execute(sql, bot)

        # update the logs with the id of the bot attack
        bot = (bot_id, next_date_id, next_time)
        sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''
        cur.execute(sql, bot)

        bot = (bot_id,)
        sql = ''' UPDATE bots SET count = count + 1 WHERE id = ? '''
        cur.execute(sql, bot)

main()
