<div align="center">

# HTTP Proxy Lab

**A Python HTTP proxy built completely from scratch to understand networking, sockets, HTTP internals, and web security.**

</div>

<div align="center">

![Python](https://img.shields.io/badge/python-3.x-blue)
![License](https://img.shields.io/github/license/Utkarsh464/http-proxy-lab)
![Last Commit](https://img.shields.io/github/last-commit/Utkarsh464/http-proxy-lab)
![GitHub Stars](https://img.shields.io/github/stars/Utkarsh464/http-proxy-lab)
![Repo Size](https://img.shields.io/github/repo-size/Utkarsh464/http-proxy-lab)

</div>

---

## What is this?

This is **not another HTTP server**.

This is a long-term educational project documenting my journey from raw TCP
sockets to a production-quality HTTP parser, logger, and forward proxy —
built entirely from scratch using only Python's standard library.

No frameworks. No `requests`. No `http.server`. Just sockets, bytes, and an
understanding of how HTTP actually works.

## Why this project exists

Modern web development hides HTTP behind frameworks. I wanted to understand
what actually happens on the wire:

- How a TCP connection is established
- How raw bytes become a request
- What `\r\n` means and why HTTP uses it
- What a forward proxy really does
- How to parse and log HTTP traffic safely

This repository is my learning journal, written in working code.

## Current Learning

This project is intentionally being built **feature-by-feature**, without any
external proxy frameworks or HTTP libraries, so I can deeply understand how
HTTP works from the socket up. Each milestone is small, understood, and
committed before the next one starts — the repository only ever contains code
that actually exists today. The journey is documented in
[docs/learning-notes.md](docs/learning-notes.md).

## Current Features

- [x] TCP socket server
- [x] Raw HTTP request parsing
- [x] Request line parsing
- [x] Header parsing
- [x] HTTP body extraction
- [x] Request object
- [x] Modular parser architecture

## Roadmap

- [x] TCP Server
- [x] Receive Raw Requests
- [x] Decode Bytes
- [x] Parse Request Line
- [x] Parse Headers
- [x] Parse Request Body
- [x] Request Object
- [ ] Parse Cookies
- [ ] Parse Query Parameters
- [ ] Parse Responses
- [ ] Forward Proxy
- [ ] Logger
- [ ] HTTPS CONNECT
- [ ] Multi-threading
- [ ] HTTP/2
- [ ] Request Interception
- [ ] Response Modification

## Latest Progress

### v0.3.0 — Request body parsing

The parser now extracts the HTTP request body. After the headers, an empty
line (`\r\n`) marks the start of the body; everything after it is collected
and stored on the `Request` object as `body`.

- `src/parser.py` now decodes the raw bytes and splits the request into lines,
  locating the empty line that separates headers from the body.
- `src/request.py` now stores a `body` attribute alongside `method`, `path`,
  `version`, and `headers`.
- `src/server.py` prints the parsed body to confirm it was received intact.

## Current capabilities

The current milestone accepts a single connection, receives one raw HTTP
request, and parses it into a `Request` object:

```
POST /login HTTP/1.1
Host: localhost:8080
Content-Type: application/x-www-form-urlencoded

user=alice&pass=secret
```

becomes

```python
request.method   # "POST"
request.path     # "/login"
request.version  # "HTTP/1.1"
request.headers  # {"Host": "localhost:8080", "Content-Type": "application/x-www-form-urlencoded"}
request.body     # "user=alice&pass=secret"
```

## Current limitations

- Handles a single connection, then exits
- `recv(1024)` only reads the first chunk of data
- Body parsing does not yet honor `Content-Length` or chunked encoding
- No response handling
- Not yet a proxy

These limitations are intentional — they are the next milestones.

## Repository tree

```
http-proxy-lab/
├── LICENSE
├── README.md
├── CHANGELOG.md
├── .gitignore
├── pyproject.toml
├── src/
│   ├── server.py
│   ├── parser.py
│   └── request.py
├── docs/
│   ├── roadmap.md
│   └── learning-notes.md
└── tests/
    └── sample_requests/
```

## Installation

Clone the repository and run it with Python 3:

```bash
git clone https://github.com/Utkarsh464/http-proxy-lab.git
cd http-proxy-lab
python3 src/server.py
```

No dependencies to install. Everything uses the Python standard library.

## Usage

In one terminal, start the server:

```bash
python3 src/server.py
```

In another terminal, send a request:

```bash
curl http://localhost:8080/hello -H "User-Agent: curl/8.0"
```

or send a raw sample request with netcat:

```bash
nc localhost 8080 < tests/sample_requests/basic-get.txt
```

## Example output

Sending a POST request to the running server:

```
Proxy server is running on http://localhost:8080
Connection from ('127.0.0.1', 43338)
0 'POST /submit HTTP/1.1'
1 'Host: localhost:8080'
2 'Content-Length: 15'
3 ''
request body
hello=world

Received request: POST /submit HTTP/1.1 {'Host': 'localhost:8080', 'Content-Length': '15'} hello=world
```

The parsed request is now a `Request` object holding the method, path,
version, headers, and body.

## Roadmap details

See [docs/roadmap.md](docs/roadmap.md) for the full journey and
[docs/learning-notes.md](docs/learning-notes.md) for the learning journal.

## License

[MIT](LICENSE)
