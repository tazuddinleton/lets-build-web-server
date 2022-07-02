# Iterative server

import socket
from time import sleep

from flask import request

SERVER_ADDRESS = (HOST, PORT) = 'localhost', 8080
REQUEST_QUEUE_SIZE = 10

def handler_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response = b'HTTP/1.1 200 OK\r\n\nHello, World!\n'
    client_connection.sendall(http_response)
    sleep(10)
    client_connection.close()

def serve_foreaver():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print(f'server started at http://{HOST}:{PORT}')

    while True:
        client_connection, client_address = listen_socket.accept()
        handler_request(client_connection)
        client_connection.close()

if __name__ == '__main__':
    serve_foreaver()