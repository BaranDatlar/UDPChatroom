from UserRegistration import authenticate_user
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

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    auth_status = authenticate_user(username, password)
    if auth_status == "Authentication successful":
        print(auth_status)
        start_client(username)
    else:
        print(auth_status)

