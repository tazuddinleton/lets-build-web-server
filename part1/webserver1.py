import socket

HOST, PORT = '', 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
print('Serving HTTP on port %s' % PORT)
while True:
    client_connection, client_address = sock.accept()
    request_data = client_connection.recv(1024)
    print(request_data.decode('utf-8'))


    http_response = """\
HTTP/1.1 200 OK 

Hello, World!
"""
        
    client_connection.sendall(bytes(http_response, 'utf-8'))
    client_connection.close()
    