from UserRegistration import authenticate_user
from PrivateChatroom import *
import socket

def start_client(username):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.1.106', 12345)  
    print(f"{username} connected to the server at {server_address}")

    initial_message = f"{username} has joined the chat".encode()
    client_socket.sendto(initial_message, server_address)

    while True:
        message = input(f"{username}: ")
        if message == 'exit':
            break
        message_to_send = f"{username}: {message}".encode()
        client_socket.sendto(message_to_send, server_address)
        data, _ = client_socket.recvfrom(1024)
        print(data.decode())

def start_private_chat(user1, user2):
    chatroom_id = create_chatroom(user1, user2)
    print(f"Private chatroom created with ID: {chatroom_id}")

    while True:
        message = input(f"{user1}: ")
        if message == 'exit':
            break
        send_message(chatroom_id, user1, message)
        messages = get_chatroom_messages(chatroom_id)
        for msg in messages:
            print(f"{msg['timestamp']} - {msg['sender']}: {msg['message']}")

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    auth_status = authenticate_user(username, password)
    if auth_status == "Authentication successful":
        print(auth_status)
        user2 = input("Enter the username of the user you want to chat with: ")
        start_private_chat(username, user2)
    else:
        print(auth_status)

