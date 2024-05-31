import datetime
from UserRegistration import Chat, Users


def create_chatroom(user1, user2):

    if not Users.find_one({"username": user2}):
        return "Error: User2 does not exist"
    
    existing_chatroom = Chat.find_one({"users": {"$all": [user1, user2]}})
    if existing_chatroom:
        return existing_chatroom['_id']

    chatroom = {
        "users": [user1, user2],
        "messages": []
    }
    result = Chat.insert_one(chatroom)
    return result.inserted_id

def send_message(chatroom_id, sender, message):
    message_data = {
        "sender": sender,
        "message": message,
        "timestamp": datetime.datetime.now()
    }
    Chat.update_one(
        {"_id": chatroom_id},
        {"$push": {"messages": message_data}}
    )

def get_chatroom_messages(chatroom_id):
    chatroom = Chat.find_one({"_id": chatroom_id})
    return chatroom['messages'] if chatroom else []