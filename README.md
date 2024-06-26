# Overview
The project implements a simple http server in python using just the http-server module. Unit tests and end-to-end tests are written to confirm its accuracy.
It currently responds to GET requests for the endpoints: "/" (root), "/hello", "/ping", "/badrequest", and "/accessdenied"
Trying to access a non-existent endpoint will result in displaying a 404 Page not found error.
It is a very basic project and primarily used for my practice.

# Usage 
Run in the terminal: python hello_ping_server.py

Go to your browser and if you use the default port, then:
+ http://localhost:8000 will display "Index Page" as a heading (h1).
+ http://localhost:8000/hello will display "Hello, World!".
+ http://localhost:8000/ping will display the current date and time.
+ http://localhost:8000/abc will display a 404 Page not found error.
+ http://localhost:8000/badrequest will display a 400 Bad Request error for a missing required query parameter "param".
+ http://localhost:8000/badrequest?param=abc will display a 200 Valid Request.
+ http://localhost:8000/accessdenied will display a 403 Forbidden error for a missing Authorization header, otherwise it will display a 200 Access Granted for a valid Authorization header.