import socket
import time
from concurrent.futures import ProcessPoolExecutor

from settings import HOST, PORT

TIMEOUT = 2
MESSAGE = b"some message"


def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(MESSAGE)
        data = s.recv(2048)
        time.sleep(TIMEOUT)
        print(f"Received message = {data!r}")


def run_tasks_in_parallel(tasks):
    with ProcessPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


if __name__ == "__main__":
    run_tasks_in_parallel([run_client for _ in range(6)])
