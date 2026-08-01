<div align="center">

# HTTP Proxy Lab

**A Python HTTP parser and proxy built completely from scratch using only Python's standard library.**

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

## Features

- TCP socket server using only the standard library
- Receives raw HTTP requests
- Decodes raw bytes to text
- Parses the HTTP request line (method, path, version)
- Parses generic HTTP headers

## Current capabilities

The current milestone accepts a single connection, receives one raw HTTP
request, and parses it into its structural parts:

```
GET /hello HTTP/1.1
Host: localhost:8080
User-Agent: curl/8.0
```

becomes

```python
{
    "Method":  "GET",
    "Path":    "/hello",
    "Version": "HTTP/1.1",
    "Host":    "localhost:8080",
    "User-Agent": "curl/8.0",
}
```

## Current limitations

- Handles a single connection, then exits
- `recv(1024)` only reads the first chunk of data
- No request body parsing yet
- No response handling
- Not yet a proxy

These limitations are intentional — they are the next milestones.

## Repository tree

```
http-proxy-lab/
├── LICENSE
├── README.md
├── .gitignore
├── src/
│   └── server.py
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

```
Server is listening on port 8080...
Connection from: ('127.0.0.1', 54321)
```

## Roadmap

From raw sockets to a production-quality proxy. See
[docs/roadmap.md](docs/roadmap.md) for the full plan and
[docs/learning-notes.md](docs/learning-notes.md) for the learning journal.

## License

[MIT](LICENSE)
