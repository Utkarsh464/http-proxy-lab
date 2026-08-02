from response import Response
from request import Request
def parse_request(data):
    data = data.decode('utf-8')
    lines = data.split("\r\n")
    body = ""
    for index, line in enumerate(lines):
        print(index, repr(line))
        if line == "":
         body = "\r\n".join(lines[index + 1:])
         break
    request_line = lines[0]
    method, path, version = request_line.split()
    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        header, separator, value = line.partition(": ")
        if separator:
            headers[header] = value
    return Request(method, path, version, headers, body)

def parse_response(data):
    data = data.decode('utf-8')
    lines = data.split("\r\n")
    body = ""
    for index, line in enumerate(lines):
        print(index, repr(line))
        if line == "":
         body = "\r\n".join(lines[index + 1:])
         break
    status_line = lines[0]
    version, status_code, reason_phrase = status_line.split(" ", 2)
    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        header, separator, value = line.partition(": ")
        if separator:
            headers[header] = value
    return Response(version, status_code, reason_phrase, headers, body)
