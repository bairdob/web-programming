import pytest
from fastapi.testclient import TestClient

import api_client
from main import app


def test_get_chat():
    chat = api_client.get_chat()

    assert 200 == chat.status_code
    assert 'text/html; charset=utf-8' == chat.headers['Content-Type']
    assert 'input id="messageInput" type="text"' in chat.text
    assert 'button id="sendButton"' in chat.text


def test_get_messages():
    messages = api_client.get_messages()

    assert 200 == messages.status_code
    assert 'application/json' == messages.headers['Content-Type']
    for message in messages.json():
        assert 'message' in message.keys()
        assert 'username' in message.keys()


def test_create_message():
    payload = {'username': 'user1', 'message': 'message from user1'}
    message = api_client.post_create_message(payload)

    assert 200 == message.status_code
    assert 'application/json' == message.headers['Content-Type']
    assert payload == message.json()


def test_messages_should_less_than_hundred():
    messages = api_client.get_messages()
    assert 100 >= len(messages.json())


def test_send_three_messages():
    payload = {'username': 'user1', 'message': 'message from user1'}
    client_headers = [
        {'User-Agent': 'Mozilla/5.0'},
        {'User-Agent': 'Chrome'},
        {'User-Agent': 'Safari'},
    ]

    messages_before_add = api_client.get_messages()
    for header in client_headers:
        api_client.post_create_message(payload, headers=header)
    messages_after_add = api_client.get_messages()

    assert len(messages_before_add.json()) == len(messages_after_add.json()) - len(client_headers)


@pytest.fixture
def client():
    return TestClient(app)


def test_websocket(client):
    message = {"username": "user1", "message": "message from user1"}
    with client.websocket_connect("/chat/ws") as websocket:
        websocket.send_json(message)
        data = websocket.receive_json()
        assert data == message


def test_recieve_message(client):
    message = {"username": "user1", "message": "message from user1"}
    with client.websocket_connect("/chat/ws") as websocket:
        websocket.send_json(message)

        with client.websocket_connect("/chat/ws") as websocket:
            data = websocket.receive_json()
            assert data == message
