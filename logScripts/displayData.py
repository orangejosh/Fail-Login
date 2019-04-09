import sys
import sqlite3
from sqlite3 import Error

args = sys.argv

def main():
    conn = create_connection("/home/pi/logData/logData.db")

    with conn:
        sql = ''' SELECT month, day, time, username, ip, city, region, country FROM logs
                    JOIN dates ON logs.date_id = dates.id
                    JOIN users ON logs.user_id = users.id 
                    JOIN locations ON logs.location_id = locations.id '''
        allLogins = getAll(conn, sql)
        getBots(allLogins)

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

def getBots(allLogins):
    prevRow = None
    for row, nextRow in zip(allLogins, allLogins[1:]):
        month = row[0]
        nextMonth = nextRow[0]

        day = row[1]
        nextDay = nextRow[1]

        time = row[2]
        nextTime = nextRow[2]

        username = row[3]
        nextUsername = nextRow[3]

        if month == nextMonth and day == nextDay and username == nextUsername:
            if closeInTime(time, nextTime):
                if row != prevRow:
                    print " "
                    print(row)

                print(nextRow)
                prevRow = nextRow

def closeInTime(time, nextTime):
        timeList = time.split(":")

        hour = int(timeList[0])
        minuite = int(timeList[1])

        nextTimeList = nextTime.split(":")

        nextHour = int(nextTimeList[0])
        nextMinuite = int(nextTimeList[1])

        if hour == nextHour and nextMinuite - minuite < 2:
            return True
        elif nextHour - 1 == hour and nextMinuite - (60 - nextMinuite) < 2:
            return True
        else:
            return False
    
main()
