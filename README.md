# Overview
The project implements a simple http server in python using just the http-server module.
It currently responds to GET requests for the endpoints: "/" (root), "/hello", and "/ping"
It is a very basic project and primarily used for my practice.

# Usage 
Run in the terminal: python hello_ping_server.py

Go to your browser and if you use the default port, then:
+ http://localhost:8000/ will display "Index Page"
+ http://localhost:8000/hello will display "Hello, World!".
+ http://localhost:8000/ping will display "Pong".

# To implement:
+ Change the ping endpoint to display dynamic data like the date and time instead
+ Unit tests to check the working of hello_ping_server.py
+ End-to-end tests to check the working of hello_ping_server.py