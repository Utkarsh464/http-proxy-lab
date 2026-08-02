import socket
from parser import parse_request
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Proxy server is running on http://localhost:8080")
try:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    request_data = client_socket.recv(1024)
    request = parse_request(request_data)
    print("request body")
    print(request.body)
    print(f"Received request: {request.method} {request.path} {request.version} {request.headers} {request.body}")
finally:
    client_socket.close()
    server_socket.close()   
