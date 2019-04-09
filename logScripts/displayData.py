import sys
import sqlite3
from sqlite3 import Error

args = sys.argv

def main():
    conn = create_connection("/home/pi/logData/logData.db")

    with conn:
        if len(args) == 1:
            sql = ''' SELECT username, COUNT(username) FROM logs 
                        JOIN users ON logs.user_id=users.id 
                        GROUP BY username 
                        ORDER BY COUNT(username) '''
            display(conn, sql)
        elif args[1].isdigit():
            print("numberic")
            sql = ''' SELECT month, day, time, username, ip, city, region, country FROM logs 
                        JOIN dates ON logs.date_id = dates.id
                        JOIN locations ON logs.location_id = locations.id
                        JOIN users ON logs.user_id = users.id
                        WHERE length(username) = ''' + args[1] + ''';'''
            display(conn, sql)

        else:
            sql = ''' SELECT month, day, time, username, ip, city, region, country FROM logs 
                        JOIN dates ON logs.date_id = dates.id
                        JOIN locations ON logs.location_id = locations.id
                        JOIN users ON logs.user_id = users.id
                        WHERE username = "''' + args[1] + '''";'''
            display(conn, sql)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None

def display(conn, sql):
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()

    for row in rows:
        print(row)
    
main()
