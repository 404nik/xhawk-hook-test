import time
from collections import defaultdict

class ChatServer:
    def __init__(self):
        self.rooms = {}  # room_id -> room_name
        self.users = defaultdict(set)  # room_id -> set of user_ids
        self.messages = defaultdict(list)  # room_id -> list of messages
        self.room_counter = 0

    def create_room(self, name: str) -> str:
        self.room_counter += 1
        room_id = str(self.room_counter)
        self.rooms[room_id] = name
        return room_id

    def join_room(self, room_id: str, user_id: str):
        if room_id not in self.rooms:
            raise ValueError('Invalid room_id')
        self.users[room_id].add(user_id)

    def leave_room(self, room_id: str, user_id: str):
        if room_id in self.users:
            self.users[room_id].discard(user_id)

    def post_message(self, room_id: str, user_id: str, text: str) -> dict:
        if room_id not in self.rooms:
            raise ValueError('Invalid room_id')
        if user_id not in self.users[room_id]:
            raise ValueError('User not in room')
        message_id = len(self.messages[room_id]) + 1
        timestamp = time.time()
        message = {'message_id': message_id, 'room_id': room_id, 'user_id': user_id, 'text': text, 'timestamp': timestamp}
        self.messages[room_id].append(message)
        return message

    def history(self, room_id: str, limit: int = 50) -> list:
        if room_id not in self.rooms:
            raise ValueError('Invalid room_id')
        return self.messages[room_id][-limit:][::-1]  # return latest N messages, newest first
