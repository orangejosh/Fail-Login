import sys
import sqlite3
from sqlite3 import Error

args = sys.argv

def main():
	# Assumes a database has ben created
    conn = create_connection("/home/pi/logData/logData.db")

    with conn:
		# No arguments returns a grouped list of the usernames used to login
        if len(args) == 1:
            sql = ''' SELECT username, COUNT(username) FROM logs 
                        JOIN users ON logs.user_id=users.id 
                        GROUP BY username 
                        ORDER BY COUNT(username) '''
            display(conn, sql)
		# If argument is a number returns usernames that are that length
        elif args[1].isdigit():
            print("numberic")
            sql = ''' SELECT month, day, time, username, ip, city, region, country FROM logs 
                        JOIN dates ON logs.date_id = dates.id
                        JOIN locations ON logs.location_id = locations.id
                        JOIN users ON logs.user_id = users.id
                        WHERE length(username) = ''' + args[1] + ''';'''
            display(conn, sql)
		# If argument is a username displays the month, day, time username, city, region, and country with that username
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
