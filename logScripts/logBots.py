import sys
import sqlite3
from sqlite3 import Error

args = sys.argv
database = args[1]  # Path to the database 
MAX_BOT_TIME = 3    # The maximum amout of time between login attempts to be considered a bot attack



def main():
    conn = create_connection(database)

    with conn:
        sql = ''' SELECT date_id, time, username FROM logs
                    JOIN dates ON logs.date_id = dates.id
                    JOIN users ON logs.user_id = users.id '''
        all_logins = get_all(conn, sql)
        log_bot_attacks(conn, all_logins)



# Connect to database
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None


# Gets all the logs. There has to be a better way.
def get_all(conn, sql):
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()


# Loops through the log looking for similiar login attemps.
def log_bot_attacks(conn, all_logins):
    last_row = None
    bot_id = None

    # Compares this row with the next to see if they look like they are from the same bot
    for row, next_row in zip(all_logins, all_logins[1:]):
        date_id = row[0]
        next_date_id = next_row[0]

        time = row[1]
        next_time = next_row[1]

        username = row[2]
        next_username = next_row[2]

        # If all criteria are met the two login are assumed to be from the same bot
        if date_id == next_date_id and username == next_username and close_in_time(time, next_time):

            # Ther first bot attack attempt
            if row != last_row:

                # Creat bot attack row in bots table
                bot = (date_id, time, next_time) 
                sql = ''' INSERT OR IGNORE INTO bots (date_id, start_time, end_time) VALUES (?, ?, ?) '''
                cur = conn.cursor()
                cur.execute(sql, bot)

                # Get the id of the bot attack row
                bot = (date_id, time)
                sql = ''' SELECT id FROM bots WHERE date_id = ? AND start_time = ? ''' 
                cur.execute(sql, bot)
                bot_id = cur.fetchall()[0][0]

                # Update the logs with the id of the bot attack
                bot = (bot_id, date_id, time)
                sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''
                cur.execute(sql, bot)

                bot = (bot_id, next_date_id, next_time)
                sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''
                cur.execute(sql, bot)

                last_row = next_row 

            # Subsequent attempt to log in by bot
            else:

                # Update the end time of the bot attack
                bot = (next_time, bot_id)
                sql = ''' UPDATE bots SET end_time = ? WHERE id = ? '''
                cur = conn.cursor()
                cur.execute(sql, bot)

                # update the logs with the id of the bot attack
                bot = (bot_id, next_date_id, next_time)
                sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''
                cur.execute(sql, bot)

                last_row = next_row
                                

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
    

main()
