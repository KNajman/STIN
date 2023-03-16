# chat_room.py - ChatRoom class for the all user chat server
from user import User


def ChatRoom(self, room, message):
    for user in self.users:
        if self.users[user].room == room:
            self.users[user].send(message)
            
def send(self, user, message):
    print(user + ": " + message)
