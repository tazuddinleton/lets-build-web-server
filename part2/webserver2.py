from email.mime import application
import io
import socket
import sys


class WsgiServer(object): 

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        listen_socket.bind(server_address)
        # Activate
        listen_socket.listen(self.request_queue_size)
        # Get server host name and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        # Return headers set by web framework/application
        self.headers_set = []
    
    def set_app(self, application):
        self.application = application
    
    def server_forever(self): 
        listen_socket = self.listen_socket
        while True:
            # New client connection
            self.client_connection, client_address = listen_socket.accept()
            # Handle one request and close the client connection. Then
            # loop over to wait for another client connection
            self.handle_one_request()
    
    def handle_one_request(self): 
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data = request_data.decode('utf-8')
        # Print formated request data 
        print('requst data: '.join(
            f'< {line}\n' for line in request_data.splitlines()
        ))

        self.parse_request(request_data)

        # Construct environment dictionary using request data
        env = self.get_environ()

        # It's time to call our application callable and get
        # back a result that will become HTTP response body
        result = self.application(env, self.start_response)
        
        # for data in result:
        #     print('result from app: ', data.decode('utf-8'))            
        # Construct a response and send it back to the client
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        # Break down the request line into components
        (
            self.request_method, # GET
            self.path,           # /hello
            self.request_version # HTTP/1.1
        ) = request_line.split()

    def get_environ(self):
        env = {}
        # Required WSGI variables
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        # Required CGI variables
        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.path
        env['SERVER_NAME'] = self.server_name
        env['SERVER_PORT'] = str(self.server_port)
        return env
    
    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Mon, 15 Jul 2023 5:54:48 GMT'),
            ('Server', 'Wsgi server 0.2')
        ]
        self.headers_set = [status, response_headers + server_headers]
        # return self.finish_response
    
    def finish_response(self, result): 
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')
            # Print formatted response data 
            print('formated result: '.join(
                f'< {line}\n' for line in response.splitlines()
            ))
            
            response_bytes = response.encode()            
            self.client_connection.sendall(response_bytes)
        finally: 
            self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = 'localhost', 8080

def make_server(server_address, application):
    server = WsgiServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')    
    module = __import__(module)        
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WsgiServer: Serving HTTP on http://{HOST}:{PORT} ...\n')
    httpd.server_forever()






