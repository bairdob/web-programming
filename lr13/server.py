import hashlib
import socket

from endpoints import *
from request_handler import Request
from responses import JSONResponse
from route import Route
from settings import HOST, PORT

routes = [
    Route('/', endpoint=index, methods=['GET']),
    Route('/not_found', endpoint=not_found, methods=['GET']),
    Route('/ping', endpoint=ping, methods=['GET']),
    Route('/json', endpoint=type_json, methods=['GET']),
    Route('/exception', endpoint=exception, methods=['GET']),
    Route('/files/mai.jpg', endpoint=image, methods=['GET']),
    Route('/files/video.mp4', endpoint=video, methods=['GET']),
    Route('/files/secret.json', endpoint=secret, methods=['GET']),
]

users = set()

sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
sct.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sct.bind((HOST, PORT))
sct.listen(1)
while True:
    conn, addr = sct.accept()
    with conn:
        print(f"Connected to {addr}")
        try:
            raw_request = conn.recv(2048)
            request = Request(raw_request)
            print(request)

            response = b''
            for route in routes:
                if route.path == request.path:
                    response = route.endpoint()

            # 404 если не найден route среди зарегистрированных
            if not response:
                response = not_found()

            if request.headers.get('User-Id') not in users:
                user = hashlib.md5(request.headers.get('User-Agent').encode()).hexdigest()
                users.add(user)
                response.set_cookie('User-Id', user)

            # TODO: решается мидлварью
            # если незарегистрированный пользователь проходит по секретному пути
            if request.headers.get('User-Id') not in users and request.path == '/files/secret.json':
                response = not_found()

            # TODO: решается мидлварью
            # если пользователь с Google Chrome пытается получить видео
            if 'Chrome' in request.headers.get('User-Agent') and response.media_type == 'video/mp4':
                response = not_found()

            conn.send(response())
        except Exception as e:
            response = JSONResponse({'detail': str(e)}, status_code=500)
            conn.send(response())
