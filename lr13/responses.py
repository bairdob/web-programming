import json
from datetime import datetime
from typing import Any


class Response:
    media_type = None
    charset = "utf-8"

    def __init__(
            self,
            content: Any = None,
            status_code: int = 200,
            media_type: str | None = None,
    ) -> None:
        self.status_code = status_code
        if media_type is not None:
            self.media_type = media_type
        self.init_headers()
        self.body = self.render(content)

    def render(self, content: Any) -> bytes | memoryview:
        if content is None:
            return b""
        if isinstance(content, (bytes, memoryview)):
            return content
        return content.encode(self.charset)  # type: ignore

    def init_headers(self) -> None:
        version = f'HTTP/1.1 {self.status_code} OK\n'.encode()
        date = f'Date: {datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")}\n'.encode()
        server = f'Server: SimpleHTTP/0.1\n'.encode()
        connection = f'Connection: socket\n'.encode()
        content_encoding = f'Content-Encoding: None\n'.encode()
        content_type = f'Content-Type: {self.media_type}\n'.encode()

        self.raw_headers = version + date + server + connection + content_encoding + content_type

    def set_cookie(self, key, value):
        self.raw_headers += f'Set-Cookie: {key}={value}\n'.encode()

    def __call__(self) -> bytes:
        return self.raw_headers + '\n'.encode() + self.body


class PlainTextResponse(Response):
    media_type = "text/plain"


class HTMLResponse(Response):
    media_type = "text/html"


class JSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return json.dumps(content,
                          ensure_ascii=False,
                          allow_nan=False,
                          indent=None,
                          separators=(",", ":"),
                          ).encode("utf-8")


class RedirectResponse(Response):
    def __init__(
            self,
            url: str,
            status_code: int = 301,
    ) -> None:
        self.url = url
        self.status_code = status_code
        super().__init__(content=b"", status_code=status_code)

    def init_headers(self):
        super().init_headers()
        location = f'Location: {self.url}\n'.encode()
        self.raw_headers += location


class FileResponse(Response):
    chunk_size = 64 * 1024

    def __init__(
            self,
            path: str,
            status_code: int = 200,
            media_type: str | None = None,
    ) -> None:
        self.path = path
        self.status_code = status_code
        if media_type is None:
            media_type = "image/jpg"
        self.media_type = media_type
        self.init_headers()

    def __call__(self) -> bytes:
        with open(self.path, "rb") as file:
            file_data = file.read()
        return self.raw_headers + '\n'.encode() + file_data
