# user.py - User class for the all user chat server

def User(self, user, message):
    if user in self.users:
        self.users[user].send(message)
    else:
        self.send("User not found")
        
    # chat room that user wants to be logged in
    chat_rooms = []
    
def add_chat_room(self, room):
    self.chat_rooms.append(room)
        
        