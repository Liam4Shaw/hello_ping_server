import unittest
import requests
import subprocess

class TestEndToEnd(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Start the server as a subprocess
        cls.server_process = subprocess.Popen(['python', 'hello_ping_server.py'])

    @classmethod
    def tearDownClass(cls):
        # Terminate the server process
        cls.server_process.terminate()

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

    def test_bad_request(self):
        response = requests.get('http://localhost:8000/badrequest')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Bad Request: Missing required query parameter "param"', response.text)

        # Test with valid query parameter
        response = requests.get('http://localhost:8000/badrequest?param=test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Valid Request')

    def test_access_denied(self):
        response = requests.get('http://localhost:8000/accessdenied')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Forbidden: Missing Authorization header', response.text)

        # Test with Authorization header
        headers = {'Authorization': 'Bearer token123'}
        response = requests.get('http://localhost:8000/accessdenied', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Access Granted')

    def test_not_found(self):
        response = requests.get('http://localhost:8000/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not Found', response.text)

if __name__ == '__main__':
    unittest.main()