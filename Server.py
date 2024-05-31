import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 12345)) 
    print("Server started and listening on port 12345")

    clients = {}

    while True:
        message, address = server_socket.recvfrom(1024)
        if address not in clients:
            clients[address] = address
            print(f"New client connected from {address}")

        print(f"Received message from {address}: {message.decode()}")

        for client in clients:
            if client != address:
                server_socket.sendto(message, client)

if __name__ == "__main__":
    start_server()
