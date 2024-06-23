from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    '''Custom HTTP request handler, handling GET requests for root (/), /hello and /ping endpoints.'''
    
    def compose_request(self) -> Dict[str, Any]:
        '''Compose and return the request dictionary from the HTTP request.'''
        url = self.path
        headers = self.headers
        method = self.command
        return {'url': url, 'headers': headers, 'method': method}
    
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


# handle_root(), handle_hello(), and handle_ping() accept the request data as parameters and return the reponse data

def handle_root(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle the root (/) endpoint.'''
    return {'code': 200, 'body': 'Index Page', 'headers': {'Content-Type': 'text/html'}}

def handle_hello(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle the /hello endpoint.'''
    return {'code': 200, 'body': 'Hello World!', 'headers': {'Content-Type': 'text/html'}}

def handle_ping(request: Dict[str, Any]) -> Dict[str, Any]:
    '''Handle the /ping endpoint.'''
    return {'code': 200, 'body': 'pong', 'headers': {'Content-Type': 'text/html'}}

def handle_404() -> Dict[str, Any]:
    '''Handle 404 Not Found errors.'''
    return {'code': 404, 'body': 'Not Found', 'headers': {'Content-Type': 'text/plain'}}

def handle_error(error: Exception) -> Dict[str, Any]:
    '''Handle internal server errors.'''
    return {'code': 500, 'body': 'Internal Server Error', 'headers': {'Content-Type': 'text/plain'}}

routes = {
    ("GET", "/"): handle_root,
    ("GET", "/hello"): handle_hello,
    ("GET", "/ping"): handle_ping
}

def route_lookup(request: Dict[str, Any]) -> Any:
    '''Lookup the route handler based on the request method and path.'''
    path = request['url']
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