
import socket
from parser import parse_request, parse_response
def get_path(request):
    path = request.path

    if path.startswith("http://"):
        path = path[7:]
        parts = path.split("/", 1)

        if len(parts) == 1:
            return "/"

        return "/" + parts[1]

    return path
def build_request(request):
    request_line = f"{request.method} {get_path(request)} {request.version}\r\n"
    header_lines = []
    for key, value in request.headers.items():
        if key.lower() == "proxy-connection":  
            continue
        header_lines.append(f"{key}: {value}")
    headers = "\r\n".join(header_lines)
    return (request_line + headers + "\r\n\r\n" + request.body).encode("utf-8")

def get_target_host_port(request):
    host_header = request.headers.get("Host")
    if not host_header:
        raise ValueError("Host header is missing in the request.")
    if ":" in host_header:
        target_host, target_port = host_header.split(":", 1)
        target_port = int(target_port)
    else:
        target_host = host_header
        target_port = 80  # Default HTTP port
    return target_host, target_port
def forward_request(target_host, target_port, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_socket:
        target_socket.connect((target_host, target_port))
        target_socket.sendall(request_data)

        response_data = receive_http_message(target_socket)

    return response_data

def receive_http_message(sock):
    buffer = b""
    while b"\r\n\r\n" not in buffer:
        data = sock.recv(1024)
        if not data:
            break
        buffer += data
    header_bytes, body_bytes = buffer.split(b"\r\n\r\n", 1)
    header_text = header_bytes.decode("utf-8")
    content_length = 0
    for line in header_text.split("\r\n"):
        if line.startswith("Content-Length:"):
            content_length = int(line.split(":", 1)[1].strip())
            break
    # Receive remaining body if needed
    while len(body_bytes) < content_length:
        data = sock.recv(1024)
        if not data:
            break
        body_bytes += data

    return header_bytes + b"\r\n\r\n" + body_bytes

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 8080))
server_socket.listen(1)
print("Proxy server is running on http://localhost:8080")
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    try:
        request_data = receive_http_message(client_socket)
        try:
            request = parse_request(request_data)
        except Exception as e:
            print(f"Failed to parse request: {e}")
            client_socket.close()
            continue
        target_host, target_port = get_target_host_port(request)
        print(f"Forwarding request to {target_host}:{target_port}")
        response_data = forward_request(target_host, target_port, build_request(request))
        try:
            response = parse_response(response_data)
        except Exception as e:
            print(f"Failed to parse response: {e}")
            client_socket.close()
            continue
        print(
            response.version,
            response.status_code,
            response.reason_phrase,
        )
        client_socket.sendall(response_data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
