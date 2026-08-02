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

### The empty-line quirk (partially fixed)

The header loop runs over every line after the request line, including the
empty line that follows the final `\r\n\r\n`. `''.partition(': ')` returns
`('', '', '')`, so that empty line becomes a junk header.

```python
# for line in lines[1:] includes '' after the final \r\n\r\n
headers[''] = ''
```

I guarded the output with `if header and value:` so the junk entry is no
longer printed:

```python
for line in lines[1:]:
    header, separator, value = line.partition(": ")
    headers[header] = value
    if header and value:
        print(f"{header}: {value}")
```

The server output is now clean:

```
Host: localhost:8080
User-Agent: curl/8.0
Accept: */*
Connection: close
```

**Worth remembering:** the guard only hides the junk — `headers[header] =
value` still runs first, so `headers['']` is still stored in the dict. Real
HTTP servers ignore lines that don't contain a colon *before* storing them.
Fixing the storage side is a future milestone.

## Current limitations

- Single connection only — the server accepts once and exits.
- `recv(1024)` truncates large requests.
- No request body parsing.
- No response handling, no proxy behaviour yet.
- `headers[''] = ''` is still stored in the dict (the print guard only hides it).

---

## 2026-08-02 — Modular parser and Request object

### What I built

Refactored the single-file `server.py` into three modules:

- `src/server.py` — networking only. Accepts a connection, reads raw bytes,
  decodes them, and hands the text off to the parser.
- `src/parser.py` — parsing only. `parse_request(data)` returns one `Request`.
- `src/request.py` — the `Request` class that stores `method`, `path`,
  `version`, and `headers`.

### Refactored parser into parser.py

```python
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
```

### Created Request class

```python
class Request:
    def __init__(self, method, path, version, headers):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
```

### Separated networking from parsing

Before, `server.py` did everything inline: receive bytes, split CRLF, parse
the request line, loop headers — all in one `try` block. Now the server only
owns the socket work:

```python
data = conn.recv(1024)
data = data.decode('utf-8')
request = parse_request(data)
```

Parsing is testable in isolation — I can call `parse_request()` with a string
and never touch a socket. That separation is the whole point of the refactor.

### Parser now returns Request objects

The parser no longer returns multiple loose values or mutates a global
`headers` dict. It builds one `Request` and returns it:

```python
request.method   # "GET"
request.path     # "/hello"
request.version  # "HTTP/1.1"
request.headers  # {"Host": "localhost:8080", ...}
```

### Learned object-oriented design

The `Request` class is my first OOP step in this project. The idea: instead
of juggling `method`, `path`, `version`, and `headers` as four separate
variables, bundle them into one object that travels together. Down the road
this object can grow a `body`, `cookies`, or helper methods without callers
changing.

### Learned why Method/Path/Version are NOT HTTP headers

This tripped me up at first. The request line and the headers both arrive in
the same raw text, so why keep them separate?

- The request line is `METHOD SP path SP HTTP-version` — it has a **fixed
  structure** (three space-separated parts).
- Headers are `name: value` pairs — a **variable set** of arbitrary lines,
  each with a colon separator.

The parser treats them differently for that reason: the request line is
unpacked positionally (`method, path, version = request_line.split()`), while
headers are discovered line by line with `partition(": ")`. Even though I
initially stored Method/Path/Version *inside* the headers dict, they are
semantically different — a header needs a colon, the request line does not.

### The empty-line quirk is now actually fixed

The old code guarded the *printing* of the junk empty header but still stored
`headers[''] = ''`. The new parser skips empty lines entirely:

```python
for line in lines[1:]:
    if not line:
        continue
```

So the junk entry is gone from the dict itself, not just hidden.

### One runtime bug I hit and fixed

I initially wrote `print('Method:', Request.method)` — capital `R`, the
class. Python raised `type object 'Request' has no attribute 'method'`. The
class is a blueprint; the parsed values live on the *instance* created by
`parse_request()`. The correct code reads from the instance:

```python
request = parse_request(data)
print('Method:', request.method)   # the instance, lowercase r
```

## Current limitations

- Single connection only — the server accepts once and exits.
- `recv(1024)` truncates large requests.
- No request body parsing.
- No response handling, no proxy behaviour yet.
- Networking and parsing are separated now, but the server still blocks on a
  single `accept()` — multi-client support is a future milestone.

---

## 2026-08-02 — Request body parsing

### What I built

The parser now extracts the HTTP request **body**. A POST request like this:

```
POST /login HTTP/1.1\r\n
Host: localhost:8080\r\n
Content-Type: application/x-www-form-urlencoded\r\n
\r\n
user=alice&pass=secret\r\n
```

now parses into a `Request` object whose `body` is `"user=alice&pass=secret"`.

### How the body is found

```python
body = ""
for index, line in enumerate(lines):
    if line == "":
        body = "\r\n".join(lines[index + 1:])
        break
```

The empty line that ends the headers is the **boundary** between headers and
body. Everything after it is the body.

### Why HTTP separates headers and body with an empty line

Headers are **metadata** — they describe the request. The body is **content** —
the actual data being sent. The empty line (`\r\n\r\n` on the wire) gives the
parser an unambiguous, unambiguous marker: the moment we see a blank line,
headers are over and the body begins. Without it, a parser would have no way
to tell where the header block ends. The body is simply *"everything that
follows the blank line"* — no length guesswork at this milestone.

### `enumerate()`

```python
for index, line in enumerate(lines):
```

`enumerate()` turns a list into pairs of `(index, value)`, so I can remember
*where* I am while I loop. I needed the index to slice the remaining lines
(`lines[index + 1:]`) once I found the empty line — a plain `for line in lines`
wouldn't give me the position.

### `repr()`

```python
print(index, repr(line))
```

`repr()` shows the string the way Python sees it, including escape characters.
So a line containing `\r` and `\n` prints as `'Host: localhost:8080'` instead
of a line break leaking into my terminal output. It makes invisible characters
visible — very useful when debugging raw network data.

### `join()`

```python
body = "\r\n".join(lines[index + 1:])
```

`split()` is the inverse of `join()`. I split on `\r\n` at the start, so I
rejoin the leftover body lines with `\r\n` to recover the body exactly as it
arrived on the wire. A body spanning multiple lines stays intact.

### Request object growth

The `Request` class gained a `body` attribute:

```python
class Request:
    def __init__(self, method, path, version, headers, body):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body
```

This is the payoff of the object-oriented design from the last milestone:
instead of threading a fifth loose variable through every function, I just add
one field to the object. The `Request` class now fully represents everything a
request carries — method, path, version, headers, and body.

### Learned to decode inside the parser

The parser now calls `data.decode('utf-8')` itself, so it accepts raw bytes
straight from the socket. That keeps the server thin — it only does networking
(`accept`, `recv`, `close`) and hands bytes straight to the parser.

## Current limitations

- Single connection only — the server accepts once and exits.
- `recv(1024)` truncates large requests.
- Body parsing ignores `Content-Length` and chunked encoding — it takes
  *everything* after the blank line, which is only correct for small bodies
  that arrive in one chunk.
- No response handling, no proxy behaviour yet.
- Networking and parsing are separated now, but the server still blocks on a
  single `accept()` — multi-client support is a future milestone.

---

## 2026-08-03 — v1.0: Basic HTTP forward proxy

### What I built

A forward proxy. The loop now does:

1. `accept()` a client.
2. `receive_http_message(client_socket)` — read the **complete** request
   (headers plus body, honoring `Content-Length`).
3. `parse_request()` — turn the bytes into a `Request` object.
4. `get_target_host_port()` — find the origin from the `Host` header.
5. `build_request()` — rewrite the request into **origin-form** and strip
   `Proxy-Connection`.
6. `forward_request()` — connect to the origin, send it, read the **complete**
   response (again honoring `Content-Length`).
7. `parse_response()` — build a `Response` object.
8. `sendall()` the raw response back to the client.

It's the full request/response round trip. That's the difference between a
parser and a proxy.

### Learned: TCP streams have no message boundaries

`recv()` returns whatever bytes have arrived — a request can span many
packets, and one packet can hold part of the next message. That's why
`Content-Length` exists: it tells the reader *exactly* how many body bytes to
wait for after the blank line. My `receive_http_message` reads headers until
`\r\n\r\n`, parses `Content-Length`, then keeps reading until it has that many
body bytes. Without this, a request split across packets would be truncated.

### Learned: absolute-form vs origin-form

A forward proxy receives requests in **absolute-form**:

```
GET http://example.com/index.html HTTP/1.1
```

because the client is telling the *proxy* which origin to fetch. When the
proxy talks to the origin directly, the request must be **origin-form**:

```
GET /index.html HTTP/1.1
```

so `get_path()` strips the `http://host` part before forwarding.

### Learned: the Proxy-Connection header

Some clients add a `Proxy-Connection` header that proxies understand but
origin servers do not. Forwarding it to the origin is wrong, so
`build_request()` drops it.

### Learned: a Response object mirrors Request

`parse_response` splits the status line (`version`, `status_code`,
`reason_phrase`) and headers, then stores the body — the mirror image of
`parse_request`. The server prints the status line after each forward so I can
see whether the origin answered.

### Current limitations

- No chunked transfer encoding — `Transfer-Encoding` bodies are not decoded.
- No HTTPS / CONNECT — `https://` requests can't be tunneled yet.
- Single-threaded — one client at a time, in a loop.
- Bodies are decoded as UTF-8, so binary bodies aren't supported.
- Header lookups are case-sensitive (`Host` must be capitalized).
- Responses without a `Content-Length` may come back truncated.
