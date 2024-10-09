from dataclasses import dataclass


@dataclass()
class Request:
    method: str
    path: str
    headers: dict
    body: bytes

    def __init__(self, raw_request: bytes):
        self.parse(raw_request)

    def parse(self, raw_request: bytes):
        raw_request = raw_request.decode('utf-8')
        lines = raw_request.split('\r\n')
        self.method, self.path, _ = lines[0].split(' ')
        self.headers = {}
        for line in lines[1:]:
            if line == '':
                break
            key, value = line.split(': ')
            self.headers[key] = value
        self.body = '\r\n'.join(lines[lines.index('') + 1:])  # type: ignore
        return self
