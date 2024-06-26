from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any
import urllib
import time

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    '''Custom HTTP request handler, handling GET requests for root (/), /hello and /ping endpoints.'''
    
    def compose_request(self) -> Dict[str, Any]:
        '''Compose and return the request dictionary from the HTTP request.'''
        url = self.path
        headers = self.headers
        method = self.command
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        path = urllib.parse.urlparse(url).path
        return {'url': url, 'headers': headers, 'method': method, 'query_params': query_params, 'path': path}
    
    
    def do_GET(self) -> None:
        '''Handle GET requests.'''
        request = self.compose_request()
        handler = route_lookup(request)
        try:
            response = handler(request)
        except Exception as error:
            response = handle_error(error)

        self.send_response(response['code'])
        for header, value in response.get('headers', {}).items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response['body'].encode('utf-8'))


# handle_root(), handle_hello(), and handle_ping() accept the request data as parameters and return the response data

def handle_root(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle the root (/) endpoint.'''
    return {'code': 200, 'body': '<h1>Index Page</h1>', 'headers': {'Content-Type': 'text/html'}}

def handle_hello(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle the /hello endpoint.'''
    return {'code': 200, 'body': 'Hello World!', 'headers': {'Content-Type': 'text/html'}}

def handle_ping(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle the /ping endpoint.'''
    response_body = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ping</title>
        <script>
            function updateTime() {
                fetch('/time')    // Make a GET request to the /time endpoint
                .then(response => response.text())
                .then(data => {
                    document.getElementById('time').innerText = data;
                });
            }
            setInterval(updateTime, 1000);    // Call updateTime every 1000 milliseconds
            window.onload = updateTime;
        </script>
    </head>
    <body>
        <h1>Current date and time:</h1>
        <p id="time"></p>
    </body>
    </html>
    '''
    return {'code': 200, 'body': response_body, 'headers': {'Content-Type': 'text/html'}}

def handle_time(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle the /time endpoint to return the current date and time.'''
    return {'code': 200, 'body': time.ctime(), 'headers': {'Content-Type': 'text/plain'}}

def handle_404(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle 404 Not Found errors.'''
    return {'code': 404, 'body': 'Not Found', 'headers': {'Content-Type': 'text/html'}}

def handle_bad_request(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle requests that result in a Bad Request (400) error.'''
    query_params = request['query_params']
    if 'param' not in query_params:
        return {'code': 400, 'body': 'Bad Request: Missing required query parameter "param".', 'headers': {'Content-Type': 'text/html'}}
    return {'code': 200, 'body': 'Valid Request', 'headers': {'Content-Type': 'text/html'}}

def handle_access_denied(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle requests that result in an Access Denied (403) error.'''
    headers = request['headers']
    if 'Authorization' not in headers:
        return {'code': 403, 'body': 'Forbidden: Missing Authorization header.', 'headers': {'Content-Type': 'text/html'}}
    return {'code': 200, 'body': 'Access Granted', 'headers': {'Content-Type': 'text/html'}}

def handle_error(error: Exception) -> Dict[str, Any]:
    '''Handle internal server errors.'''
    return {'code': 500, 'body': 'Internal Server Error', 'headers': {'Content-Type': 'text/html'}}

routes = {
    ("GET", "/"): handle_root,
    ("GET", "/hello"): handle_hello,
    ("GET", "/ping"): handle_ping,
    ("GET", "/time"): handle_time,
    ("GET", "/badrequest"): handle_bad_request,
    ("GET", "/accessdenied"): handle_access_denied
}

def route_lookup(request: Dict[str, Any]) -> Any:
    '''Lookup the route handler based on the request method and path.'''
    path = request['path']
    method = request['method']
    route_key = (method, path)
    # If the route_key is found in the routes dictionary, return corresponding handler function, else return the handle_404 function
    return routes.get(route_key, handle_404)

def run(server_class: type = HTTPServer, handler_class: type = CustomHTTPRequestHandler, port: int = 8000) -> None:
    ''' Run the server.

    Referenced from: https://docs.python.org/3/library/http.server.html
    
    Keyword Arguments:
    server_class -- The server class to use, default is HTTPServer.
    handler_class -- The request handler class, where the default is CustomHTTPRequestHandler, a subclass(defined above) of BaseHTTPRequestHandler.
    port -- the port on which the server will listen for incoming requests, for default 8000, it will listen on localhost:8000
    ''' 
    server_address = ('', port)    # '' means the server will accept requests from any IP address
    
    # Create an instance of the server (stored in variable httpd) using the server_class (which defaults to HTTPServer)
    # Use server_address as the address and handler_class (which defaults to MyHTTPRequestHandler) to handle incoming requests
    httpd = server_class(server_address, handler_class)

    print(f"Server running on port: {port}")
    
    # Run until explicitly stopped
    httpd.serve_forever()

if __name__ == "__main__":
    run()
