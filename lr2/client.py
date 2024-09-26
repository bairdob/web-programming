import datetime
import logging
import socket
import time

from settings import HOST, PORT

logging.basicConfig(
    filename='client_conn.log',
    filemode='w',
    format='%(asctime)s.%(msecs)03d - %(message)s',
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

TIMEOUT = 2
MESSAGE = b"Bair Dobylov M3O-207M"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    logger.info(f"Connected to {HOST}:{PORT}")

    time.sleep(TIMEOUT)

    now = datetime.datetime.now()
    logger.info(f"Sending MESSAGE = {MESSAGE}")
    s.sendall(MESSAGE)

    data = s.recv(1024)
    logger.info(f"Received MESSAGE = {data!r}")
