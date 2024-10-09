from responses import *


def ping():
    return PlainTextResponse(content='PONG', media_type='text/plain')


def not_found():
    return HTMLResponse(content='<h1>Page not found</h1>', status_code=404)


def type_json():
    return JSONResponse(content={"message": "Hello, world!"})


def exception():
    raise Exception("Something went wrong")


def image():
    return FileResponse(path='./static/mai.jpg')


def video():
    return FileResponse(path='./static/video.mp4', media_type='video/mp4')


def index():
    return RedirectResponse(url='/plain_text')


def secret():
    return FileResponse(path='./static/secret.json', media_type='application/json')
