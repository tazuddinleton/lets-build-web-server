# concurrent server

import os
import socket 
from time import sleep
import signal
import errno



SERVER_ADDRESS = (HOST, PORT) = 'localhost', 8080
REQUEST_QUEUE_SIZE = 5

def grim_reaper(signum, frame):
    pid, status = os.wait()
    print(
        'Child {pid} terminated with status {status}\n'.format(
            pid=pid, status=status
        )
    )

def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(
        'child PID: {pid}, parent PID: {ppid}'.format(
            pid = os.getpid(),
            ppid = os.getppid()
        )
    )
    print(request.decode())
    http_response = b'HTTP/1.1 200 OK\r\n\nHello world!\n'
    client_connection.sendall(http_response)
    sleep(10)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('started http server at http://{HOST}:{PORT}')
    print('Parent PID (PPID): {pid}\n'.format(pid = os.getpid()))

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            print(code, msg)
            if code == errno.EINTR:
                continue
            else:
                raise
        pid = os.fork()
        if pid == 0: # Child process
            listen_socket.close() # Close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else: # Parent process
            client_connection.close() # Close parent copy and loop over

if __name__ == '__main__':
    serve_forever()

        
