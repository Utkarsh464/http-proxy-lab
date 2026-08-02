import socket
from parser import parse_request
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
headers = {}

try:
    server_socket.listen(1)
    print('Server is listening on port 8080...')
    conn, addr = server_socket.accept()
    print('Connection from:', addr)
    data = conn.recv(1024)
    data = data.decode('utf-8')
    print('Received data:', data)
    request = parse_request(data)
    print('Method:', request.method)
    print('Path:', request.path)
    print('Version:', request.version)
    print('Headers:', request.headers)
except Exception as e:
    print('Error:', e)