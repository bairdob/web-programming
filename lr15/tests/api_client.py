import requests

API_URL = 'http://localhost:8000'


def get_chat():
    return requests.get(f'{API_URL}/chat')


def get_messages():
    return requests.get(f'{API_URL}/chat/messages')


def post_create_message(payload: dict, headers: dict = None):
    return requests.post(f'{API_URL}/chat/messages', json=payload, headers=headers)
