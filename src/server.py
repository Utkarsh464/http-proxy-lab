import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))

try:
    server_socket.listen(1)
    print('Server is listening on port 8080...')

    conn, addr = server_socket.accept()
    print('Connection from:', addr)

    data = conn.recv(1024)
    data = data.decode('utf-8')

    lines = data.split("\r\n")

    request_line = lines[0]

    method, path, version = request_line.split()

    print('Method:', method)
    print('Path:', path)
    print('Version:', version)

except Exception as e:
    print("Error:", e)
