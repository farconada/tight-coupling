# app-via-grpc/app.py
import grpc
import os
import users_pb2
import users_pb2_grpc
import time

def get_users():
    with grpc.insecure_channel(os.environ['GRPC_SERVER']) as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUsers(users_pb2.Empty())
    return response.users

if __name__ == '__main__':
    time.sleep(30)
    users = get_users()
    print("Users (accessed via gRPC):")
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
