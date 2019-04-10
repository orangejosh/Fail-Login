import sys
import sqlite3
from sqlite3 import Error

args = sys.argv
database = args[1]

def main():
    conn = create_connection(database)

    with conn:
        sql = ''' SELECT month, day, time, username, ip, city, region, country, date_id FROM logs
                    JOIN dates ON logs.date_id = dates.id
                    JOIN users ON logs.user_id = users.id 
                    JOIN locations ON logs.location_id = locations.id '''
        allLogins = getAll(conn, sql)
        logBotAttacks(conn, allLogins)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None


def getAll(conn, sql):
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()

def logBotAttacks(conn, allLogins):
    lastRow = None
    bot_id = None
    for row, nextRow in zip(allLogins, allLogins[1:]):
        month = row[0]
        nextMonth = nextRow[0]

        day = row[1]
        nextDay = nextRow[1]

        time = row[2]
        nextTime = nextRow[2]

        username = row[3]
        nextUsername = nextRow[3]

        date_id = row[8]
        nextDate_id = nextRow[8]

        if month == nextMonth and day == nextDay and username == nextUsername and closeInTime(time, nextTime):
            if row != lastRow:
                bot = (date_id, time, nextTime) 
                sql = ''' INSERT OR IGNORE INTO bots (date_id, start_time, end_time) VALUES (?, ?, ?) '''
                cur = conn.cursor()
                cur.execute(sql, bot)

                bot = (date_id, time)
                sql = ''' SELECT id FROM bots WHERE date_id = ? AND start_time = ? ''' 
                cur.execute(sql, bot)
                bot_id = cur.fetchall()[0][0]

                bot = (bot_id, date_id, time)
                sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''
                cur.execute(sql, bot)

                bot = (bot_id, nextDate_id, nextTime)
                sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''
                cur.execute(sql, bot)

                lastRow = nextRow 
            else:
                bot = (nextTime, bot_id)
                sql = ''' UPDATE bots SET end_time = ? WHERE id = ? '''
                cur = conn.cursor()
                cur.execute(sql, bot)

                bot = (bot_id, nextDate_id, nextTime)
                sql = ''' UPDATE logs SET bot_id = ? WHERE date_id = ? AND time = ? '''
                cur.execute(sql, bot)

                lastRow = nextRow
                                

def closeInTime(time, nextTime):
        timeList = time.split(":")

        hour = int(timeList[0])
        minuite = int(timeList[1])

        nextTimeList = nextTime.split(":")

        nextHour = int(nextTimeList[0])
        nextMinuite = int(nextTimeList[1])

        if hour == nextHour and nextMinuite - minuite < 2:
            return True
        elif nextHour - 1 == hour and nextMinuite + (60 - minuite) < 2:
            return True
        else:
            return False
    
main()
