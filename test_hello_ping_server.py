import unittest
from hello_ping_server import CustomHTTPRequestHandler
from http.server import HTTPServer
import threading
import requests

class TestHTTPServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('localhost', 8000), CustomHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_root(self):
        response = requests.get('http://localhost:8000/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Index Page</h1>', response.text)

    def test_hello(self):
        response = requests.get('http://localhost:8000/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hello World!')

    def test_ping(self):
        response = requests.get('http://localhost:8000/ping')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Current date and time:</h1>', response.text)

    def test_time(self):
        response = requests.get('http://localhost:8000/time')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text.strip())  # Check if the response text is non-empty

    def test_not_found(self):
        response = requests.get('http://localhost:8000/unknown')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.text, 'Not Found')

if __name__ == '__main__':
    unittest.main()