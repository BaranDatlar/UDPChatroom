from UserRegistration import authenticate_user
import socket
import json
import threading

def start_private_chat(username, server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    user2 = input("Enter the username of the user you want to chat with: ")

    # Chatroom oluşturma isteği gönder
    create_request = {
        "action": "create_chatroom",
        "user1": username,
        "user2": user2
    }
    client_socket.sendto(json.dumps(create_request).encode(), server_address)

    # Sunucudan cevap bekle
    data, _ = client_socket.recvfrom(1024)
    response = json.loads(data.decode())
    
    if response["status"] == "success":
        chatroom_id = response["chatroom_id"]
        print(f"Private chatroom created with ID: {chatroom_id}")
    else:
        print(response["message"])
        return

    # Gelen mesajları dinlemek için ayrı bir iş parçacığı başlat
    def listen_for_messages():
        while True:
            try:
                data, _ = client_socket.recvfrom(1024)
                response = json.loads(data.decode())
                if response["status"] == "success" and "messages" in response:
                    messages = response["messages"]
                    for msg in messages:
                        print(f"{msg['timestamp']} - {msg['sender']}: {msg['message']}")
                elif "message" in response:
                    print(response["message"])
            except Exception as e:
                print(f"Error receiving message: {e}")

    listener_thread = threading.Thread(target=listen_for_messages, daemon=True)
    listener_thread.start()

    while True:
        message = input(f"{username}: ")
        if message == 'exit':
            break
        send_request = {
            "action": "send_message",
            "chatroom_id": chatroom_id,
            "sender": username,
            "message": message
        }
        client_socket.sendto(json.dumps(send_request).encode(), server_address)
        
        # Mesajları güncelle ve ekrana yaz
        get_messages_request = {
            "action": "get_messages",
            "chatroom_id": chatroom_id
        }
        client_socket.sendto(json.dumps(get_messages_request).encode(), server_address)


if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    auth_status = authenticate_user(username, password)
    if auth_status == "Authentication successful":
        print(auth_status)
        server_address = ('192.168.1.106', 12345)  # Sunucunun IP ve portu
        start_private_chat(username, server_address)
    else:
        print(auth_status)
