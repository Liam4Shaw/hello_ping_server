from http.server import HTTPServer, BaseHTTPRequestHandler

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    '''Custom HTTP request handler, handling GET requests for /hello and /ping endpoints.'''

    def do_GET(self) -> None:
        """Handle GET requests.
        
        Respond with 200 (OK) status code and "Hello, World!" header for the /hello endpoint.
        Respond with 200 (OK) status code and "Pong" header for the /ping endpoint.
        Respond with 404 Page Not Found error for any other paths.
        """
        
        # TODO: Change implementation of ping endpoint to repond with dynamic date like date & time

        if self.path == "/hello":
            self.send_response(200)  # Send an HTTP status code 200 (OK)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(b"Hello, World!")  # Write the response body
        elif self.path == "/ping":
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(b"Pong")
        else:
            self.send_response(404)  
            self.end_headers()


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