# app-via-web-service/app.py
import requests
import os
import time

def get_users():
    response = requests.get(f"{os.environ['WEB_SERVICE_URL']}/users")
    return response.json()

if __name__ == '__main__':
    time.sleep(30)
    users = get_users()
    print("Users (accessed via web service):")
    for user in users:
        print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
