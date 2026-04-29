import pytest
from server import ChatServer

@pytest.fixture
def chat_server():
    return ChatServer()

def test_create_and_join_room(chat_server):
    room_id = chat_server.create_room('General')
    chat_server.join_room(room_id, 'user1')
    assert 'user1' in chat_server.users[room_id]

def test_post_message(chat_server):
    room_id = chat_server.create_room('General')
    chat_server.join_room(room_id, 'user1')
    message = chat_server.post_message(room_id, 'user1', 'Hello!')
    assert message['text'] == 'Hello!'
    assert message['user_id'] == 'user1'

def test_history(chat_server):
    room_id = chat_server.create_room('General')
    chat_server.join_room(room_id, 'user1')
    chat_server.post_message(room_id, 'user1', 'Hello!')
    chat_server.post_message(room_id, 'user1', 'World!')
    history = chat_server.history(room_id)
    assert len(history) == 2
    assert history[0]['text'] == 'World!'

def test_multi_user_posts(chat_server):
    room_id = chat_server.create_room('General')
    chat_server.join_room(room_id, 'user1')
    chat_server.join_room(room_id, 'user2')
    chat_server.post_message(room_id, 'user1', 'Hello from user1!')
    chat_server.post_message(room_id, 'user2', 'Hello from user2!')
    history = chat_server.history(room_id)
    assert history[0]['text'] == 'Hello from user2!'
    assert history[1]['text'] == 'Hello from user1!'

def test_leave_room(chat_server):
    room_id = chat_server.create_room('General')
    chat_server.join_room(room_id, 'user1')
    chat_server.leave_room(room_id, 'user1')
    with pytest.raises(ValueError):
        chat_server.post_message(room_id, 'user1', 'This should fail')

def test_history_limit(chat_server):
    room_id = chat_server.create_room('General')
    chat_server.join_room(room_id, 'user1')
    for i in range(60):
        chat_server.post_message(room_id, 'user1', f'Message {i}')
    history = chat_server.history(room_id, limit=50)
    assert len(history) == 50
    assert history[0]['text'] == 'Message 59'


def test_post_to_nonexistent_room(chat_server):
    with pytest.raises(ValueError):
        chat_server.post_message('invalid_room', 'user1', 'Hello!')


def test_post_without_joining(chat_server):
    room_id = chat_server.create_room('General')
    with pytest.raises(ValueError):
        chat_server.post_message(room_id, 'user1', 'Hello!')
