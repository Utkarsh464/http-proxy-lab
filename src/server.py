import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))

try:
    server_socket.listen(1)
    print('Server is listening on port 8080...')

    conn, addr = server_socket.accept()
    print('Connection from:', addr)

    data = conn.recv(1024)
    print('Received:', data)

except Exception as e:
    print("Error:", e)
