import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))

host, port = sock.getsockname()[:2]
print(host, port)

sock.sendall(b'test')
data = sock.recv(1024)
print(data.decode())


