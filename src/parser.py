from request import Request
def parse_request(data):
    lines = data.split("\r\n")
    request_line = lines[0]
    method, path, version = request_line.split()
    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        header, separator, value = line.partition(": ")
        if separator:
            headers[header] = value
    return Request(method, path, version, headers)
