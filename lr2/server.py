import asyncio
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


async def handle_client(client):
    loop = asyncio.get_event_loop()
    addr = client.getpeername()
    with client:
        logger.info(f"Connected by {addr}")
        while True:
            data = await loop.sock_recv(client, 2048)
            logger.info(f"Received data: {data}")
            if not data:
                break
            time.sleep(TIMEOUT)
            message = f"Server created by Bair Dobylov M3O-207M. {data.decode()[::-1]}"
            await loop.sock_sendall(client, str.encode(message))
            logger.info(f"Sent data: {message}")
        logger.info("Client disconnected")


async def run_server():
    logger.info("Server started")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    s.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(s)
        loop.create_task(handle_client(client))


if __name__ == "__main__":
    asyncio.run(run_server())
