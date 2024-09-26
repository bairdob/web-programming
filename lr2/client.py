import datetime
import socket
import time

from settings import HOST, PORT

TIMEOUT = 2
MESSAGE = b"some message"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    now = datetime.datetime.now()
    s.sendall(MESSAGE)
    data = s.recv(2048)
    time.sleep(TIMEOUT)
    print(f"Received message = {data!r}")
