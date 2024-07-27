# web-service/app.py
from flask import Flask, jsonify
import psycopg2
import os
import grpc
from concurrent import futures
import users_pb2
import users_pb2_grpc
import time

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )
    return conn

def get_users_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return [{'id': user[0], 'name': user[1], 'email': user[2]} for user in users]

@app.route('/users')
def get_users():
    users = get_users_from_db()
    return jsonify(users)

class UserServicer(users_pb2_grpc.UserServiceServicer):
    def GetUsers(self, request, context):
        users = get_users_from_db()
        return users_pb2.UserList(users=[
            users_pb2.User(id=user['id'], name=user['name'], email=user['email'])
            for user in users
        ])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    time.sleep(20)
    from threading import Thread
    Thread(target=serve).start()
    app.run(host='0.0.0.0', port=8080)
