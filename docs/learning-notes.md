# Learning Notes

Raw notes from today's session. Written as I learned, not after.

## What I built

A minimal TCP server in `src/server.py` that receives one raw HTTP request
and parses the request line and headers — entirely from scratch.

## What I learned

### Building the first TCP server

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

- `socket()` creates a socket. `AF_INET` says "IPv4", `SOCK_STREAM` says
  "reliable, ordered, two-way byte stream" (TCP).
- `bind(('localhost', 8080))` attaches the socket to an address and port.
  The two-tuple `(host, port)` is the socket's identity on the network.
- `listen(1)` tells the OS this is a *server* socket that can accept
  connections. The `1` is the size of the OS backlog queue.
- `accept()` blocks until a client connects. It returns a **new** socket
  (`conn`) for talking to that client, plus the client's address (`addr`).
  The listening socket itself stays open for the next `accept()`.
- `recv(1024)` reads up to 1024 bytes of data from the connection.

The mental model I walked away with: a server socket is a *doorbell*.
`accept()` answers it, and the socket you get back is the *conversation*.

### HTTP requests

A raw HTTP/1.1 request looks like this on the wire:

```
GET / HTTP/1.1\r\n
Host: localhost:8080\r\n
User-Agent: curl/8.0\r\n
\r\n
```

- The first line is the **request line**: `METHOD SP path SP HTTP-version`.
- Everything after it is **headers**: `name: value`.
- An empty line (`\r\n`) separates headers from the body.

### CRLF

HTTP lines are separated by **CRLF** — a carriage return (`\r`, `0x0D`)
followed by a line feed (`\n`, `0x0A`). Not just `\n`. This is a legacy of
typewriters and is one of those details frameworks hide from you. I encoded
the sample request (`tests/sample_requests/basic-get.txt`) with real CRLF
bytes to make that concrete.

### Parsing the request line

```python
lines = data.split("\r\n")
request_line = lines[0]
method, path, version = request_line.split()
```

- `data.decode('utf-8')` turns the raw `bytes` into `str`.
- `split("\r\n")` breaks the request into lines.
- `split()` (no argument) on the request line splits on any whitespace.

### Parsing headers

```python
for line in lines[1:]:
    header, separator, value = line.partition(": ")
    headers[header] = value
```

- I first reached for `split(": ")`, but `partition` is better here.

### `partition()` vs `split()`

```python
"Host: localhost:8080".split(": ")     # ['Host', 'localhost:8080']
"Host: localhost:8080".partition(": ") # ('Host', ': ', 'localhost:8080')
```

- `partition(": ")` splits on the **first** occurrence and always returns
  exactly three parts: `(before, separator, after)`.
- `split(": ")` splits on **every** occurrence — a value that itself
  contains `": "` (like an IPv6 address or a cookie header) would be torn
  apart. `partition` is the correct tool here.

### Sequence unpacking

```python
method, path, version = request_line.split()
```

This is tuple unpacking: `split()` returns a list, and Python unpacks it
into three names in one line. Cleaner and more readable than indexing.

### Why `recv(1024)` is insufficient

`recv(1024)` reads *up to* 1024 bytes and returns whatever is currently
available. Two problems:

1. A request larger than 1024 bytes gets **truncated**.
2. A request split across network packets may arrive in **multiple chunks**,
   and one `recv()` call will only see the first chunk.

Proper handling needs a read loop that accumulates bytes until the end of
the request is found. That is a future milestone.

## Findings from today

Parsing the headers with the current loop produces one quirk: the empty
line after the final `\r\n` becomes an empty header entry.

```python
# for line in lines[1:] includes '' after the final \r\n\r\n
headers[''] = ''
```

```python
>>> print(headers)
{'Method': 'GET', 'Path': '/', 'Version': 'HTTP/1.1',
 'Host': 'localhost:8080', 'User-Agent': 'curl/8.0',
 'Accept': '*/*', 'Connection': 'close', '': ''}
```

`''.partition(': ')` returns `('', '', '')`, so the empty line is stored as
an empty header. Worth remembering — real HTTP servers explicitly ignore
lines that don't contain a colon. This is exactly the kind of edge case that
shows up when you parse HTTP by hand.

## Current limitations

- Single connection only — the server accepts once and exits.
- `recv(1024)` truncates large requests.
- No request body parsing.
- No response handling, no proxy behaviour yet.
- Empty trailing line becomes a junk header (see above).
