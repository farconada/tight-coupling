# app-direct-access/app.py
import psycopg2
import os
import time

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    return conn

def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

if __name__ == '__main__':
    # sleep for 30s
    time.sleep(30)

    users = get_users()
    print("Users (accessed directly from database):")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
