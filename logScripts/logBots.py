import sys
import sqlite3
from sqlite3 import Error

args = sys.argv
database = args[1]  # Path to the database 
MAX_BOT_TIME = 3    # The maximum amout of time between login attempts to be considered a bot attack



def main():
    conn = create_connection(database)
    cur = conn.cursor()

    last_row = None
    bot_id = None

    with conn:
        sql = ''' SELECT date_id, time, username FROM logs
                    JOIN dates ON logs.date_id = dates.id
                    JOIN users ON logs.user_id = users.id '''
        cur.execute(sql)

        row = next(cur, None)
        while row is not None:
            next_row = next(cur, None)
            if next_row is None:
                break
            
            date_id = row[0]
            next_date_id = next_row[0]

            time = row[1]
            next_time = next_row[1]

            username = row[2]
            next_username = next_row[2]

			# Tests if this row and next_row meet the criteria for a bot
            if date_id == next_date_id and username == next_username and close_in_time(time, next_time):
                if last_row != row:
                    bot_id = create_bot(conn, bot_id, date_id, next_date_id, time, next_time)
                else:
                    update_bot(conn, bot_id, next_date_id, next_time)

                last_row = next_row
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


# Create a bot entry i the database with id, start time, end_time, and count
def create_bot(conn, bot_id, date_id, next_date_id, time, next_time):
    cur = conn.cursor()

	# Is duplicate
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


def update_bot(conn, bot_id, next_date_id, next_time):
    if bot_id is not None:
        cur = conn.cursor()

		# Update end_time of bot
        bot = (next_time, bot_id)
        sql = ''' UPDATE bots SET end_time = ? WHERE id = ? '''
        cur.execute(sql, bot)

        # Update the logs with the id of the bot attack
        bot = (bot_id, next_date_id, next_time)
        sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''
        cur.execute(sql, bot)

        bot = (bot_id,)
        sql = ''' UPDATE bots SET count = count + 1 WHERE id = ? '''
        cur.execute(sql, bot)

main()
