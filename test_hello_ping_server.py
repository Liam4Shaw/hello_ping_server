import unittest
from hello_ping_server import handle_root, handle_hello, handle_ping, handle_404, handle_bad_request, handle_access_denied, handle_error

class TestHTTPHandlers(unittest.TestCase):

    def setUp(self):
        self.request = {'method': 'GET', 'headers': {}}
    
    def tearDown(self):
        pass
        
    def test_handle_root(self):
        self.request['url'] = '/'
        response = handle_root(self.request)
        self.assertEqual(response['code'], 200)
        self.assertIn('<h1>Index Page</h1>', response['body'])
        self.request['url'] = ''
        response = handle_root(self.request)
        self.assertEqual(response['code'], 200)
        self.assertIn('<h1>Index Page</h1>', response['body'])
    
    def test_handle_hello(self):
        self.request['url'] = '/hello'
        response = handle_hello(self.request)
        self.assertEqual(response['code'], 200)
        self.assertIn(response['body'], 'Hello World!')

    def test_handle_ping(self):
        self.request['url'] = '/ping'
        response = handle_ping(self.request)
        self.assertEqual(response['code'], 200)
        self.assertIn('<h1>Current date and time:</h1>', response['body'])
    
    def test_handle_404(self):
        self.request['url'] = '/notfound'
        response = handle_404(self.request)
        self.assertEqual(response['code'], 404)
        self.assertIn('Page Not Found', response['body'])

    def test_handle_bad_request(self):
        self.request['url'] = '/badrequest'
        self.request['query_params'] = {}
        response = handle_bad_request(self.request)
        self.assertEqual(response['code'], 400)
        self.assertIn('Bad Request', response['body'])
        # When param is given
        self.request['query_params']['param'] = ''
        response = handle_bad_request(self.request)
        self.assertEqual(response['code'], 200)
        self.assertIn('Valid Request', response['body'])
        
    def test_handle_access_denied(self):
        self.request['url'] = '/accessdenied'
        response = handle_access_denied(self.request)
        self.assertEqual(response['code'], 403)
        self.assertIn('Forbidden: Missing Authorization header', response['body'])
        # When authorization header is present
        self.request['headers']['Authorization'] = 'Bearer token123'
        response = handle_access_denied(self.request)
        self.assertEqual(response['code'], 200)
        self.assertIn('Access Granted', response['body'])

     # Test for handle_error function
    def test_handle_error(self):
        # Simulate an internal server error by passing None as request
        response = handle_error(None)
        self.assertEqual(response['code'], 500)
        self.assertIn('Internal Server Error', response['body'])
        
if __name__ == '__main__':
    unittest.main()