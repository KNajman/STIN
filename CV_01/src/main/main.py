# main implementation of chat server room
from chat_room import ChatRoom
from user import User


if __name__ == "__main__":
    ChatRoom = ChatRoom("general")
    ChatRoom = ChatRoom("sports")
    print("Welcome to the chat server")

    while (True):
        print("Enter your name:")
        name = input()
        # create a new user or validate an existing user
        if name not in User.users:
            chat_user = User(name)
        else:
            chat_user = User.users[name]

        print("Which chat room would you like to join?")
        room = input()
        if room not in ChatRoom.chat_rooms:
            print("Chat room not found")
            continue
        else:
            User.add_chat_room(room)

        print("Message:")
        message = input()

        # send the message to the chat room
        ChatRoom.chat_room(user, message)
