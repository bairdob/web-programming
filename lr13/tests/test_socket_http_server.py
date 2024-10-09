import unittest

import requests

SERVER_PATH_TEMPLATE = 'http://127.0.0.1:65432{path}'


class TestSocketServerHeaders(unittest.TestCase):
    def test_allowed_headers(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/'))
        self.assertIn('Server', response.headers)
        self.assertIn('Date', response.headers)
        self.assertIn('Content-Type', response.headers)
        self.assertIn('Connection', response.headers)
        self.assertIn('Content-Encoding', response.headers)


class TestSocketServerStatusCodes(unittest.TestCase):
    def test_200_status_code(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/ping'))
        self.assertEqual(response.status_code, 200)

    def test_404_status_code(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/not_found'))
        self.assertEqual(response.status_code, 404)

    def test_500_status_code(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/exception'))
        self.assertEqual(response.status_code, 500)

    def test_301_status_code(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/'), allow_redirects=False)
        self.assertEqual(response.status_code, 301)
        self.assertIn('Location', response.headers)


class TestSocketServerContentType(unittest.TestCase):

    def test_plain_text_content_type(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/ping'))
        self.assertEqual(response.text, 'PONG')
        self.assertEqual(response.headers['Content-Type'], 'text/plain')

    def test_html_content_type(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/not_found'))
        self.assertIn('<h1>Page not found</h1>', response.text)
        self.assertEqual(response.headers['Content-Type'], 'text/html')

    def test_json_content_type(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/json'))
        self.assertEqual(response.text, '{"message":"Hello, world!"}')
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_image_content_type(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/files/mai.jpg'))
        self.assertEqual(response.headers['Content-Type'], 'image/jpg')
        self.assertEqual(len(response.content), 485097)

    def test_video_content_type(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/files/video.mp4'))
        self.assertEqual(response.headers['Content-Type'], 'video/mp4')
        self.assertEqual(len(response.content), 1570024)


class TestSocketServerCookies(unittest.TestCase):
    def test_return_cookie_user_id(self):
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/'))
        self.assertIn('User-Id', response.cookies.get_dict())

    def test_get_secret_file_by_cookie(self):
        response_with_cookie = requests.get(SERVER_PATH_TEMPLATE.format(path='/'))
        user_id = response_with_cookie.cookies.get_dict()
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/files/secret.json'), headers=user_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"secret": "supersecret"})


class TestSocketServerUserAgent(unittest.TestCase):
    def test_no_return_mp4_for_google_chrome(self):
        chrome_user_agent = {"User-Agent": "Chrome/58"}
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/files/video.mp4'), headers=chrome_user_agent)

        self.assertEqual(response.status_code, 404)

    def test_return_mp4_for_firefox(self):
        firefox_user_agent = {"User-Agent": "Firefox/58"}
        response = requests.get(SERVER_PATH_TEMPLATE.format(path='/files/video.mp4'), headers=firefox_user_agent)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'video/mp4')
