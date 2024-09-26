import logging
import socket
import time

from settings import HOST, PORT

logging.basicConfig(
    filename='server_conn.log',
    filemode='w',
    format='%(asctime)s.%(msecs)03d - %(message)s',
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

TIMEOUT = 1

logger.info("Server started")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        logger.info(f"Connected by {addr}")
        while True:
            data = conn.recv(2048)
            logger.info(f"Received data: {data}")
            if not data:
                break
            time.sleep(TIMEOUT)
            message = f"Server created by Bair Dobylov M3O-207M. {data.decode()[::-1]}"
            conn.sendall(str.encode(message))
            logger.info(f"Sent data: {message}")
        logger.info("Client disconnected")
