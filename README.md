<div align="center">

# HTTP Proxy Lab

**A Python HTTP forward proxy built completely from scratch to understand networking, sockets, HTTP internals, and web security.**

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

- [x] TCP socket server (accept loop, sequential clients)
- [x] Raw HTTP request parsing
- [x] Full request reading driven by `Content-Length`
- [x] Response parsing (`Response` object)
- [x] Full response reading driven by `Content-Length`
- [x] Origin-form path rewriting (absolute-form → `/path`)
- [x] `Proxy-Connection` header stripped before forwarding
- [x] Request forwarding to the origin server
- [x] Response relay back to the client

## Roadmap

- [x] TCP Server
- [x] Receive Raw Requests
- [x] Decode Bytes
- [x] Parse Request Line
- [x] Parse Headers
- [x] Parse Request Body
- [x] Request Object
- [x] Parse Responses
- [x] Forward Proxy
- [ ] Parse Cookies
- [ ] Parse Query Parameters
- [ ] Logger
- [ ] HTTPS CONNECT
- [ ] Multi-threading
- [ ] HTTP/2
- [ ] Request Interception
- [ ] Response Modification

## Latest Progress

### v1.0 — Basic HTTP forward proxy

The project is now a real forward proxy. It accepts a client connection, reads
the complete request, parses it, rewrites it to origin-form, strips the
non-standard `Proxy-Connection` header, forwards it to the origin server,
reads the complete response, and relays it back to the client.

- `src/server.py` — the proxy loop: accept → read full request → parse →
  rewrite → forward → read full response → parse → send back.
- `src/parser.py` — now parses **both** requests (`parse_request`) and
  responses (`parse_response`).
- `src/response.py` — new `Response` object (version, status code, reason
  phrase, headers, body).
- `Content-Length` is honored when reading both requests and responses, so
  bodies split across multiple packets arrive intact.

## Current capabilities

A request sent through the proxy:

```
curl -x http://localhost:8080 http://example.com/index.html
```

arrives at the origin server as an origin-form request (no absolute URL, no
`Proxy-Connection` header):

```
GET /index.html HTTP/1.1
Host: example.com
User-Agent: curl/8.0
```

and the origin's response is relayed back to the client untouched.

## Current limitations

- No chunked transfer encoding (`Transfer-Encoding` bodies are not decoded)
- No HTTPS / CONNECT tunneling
- No streaming
- No multi-threading — clients are handled one at a time, sequentially
- No HTTP/2
- No response modification or interception
- Body bytes are decoded as UTF-8, so binary bodies are not supported
- Header lookups are case-sensitive (e.g., `Host` must be capitalized)

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
│   ├── request.py
│   └── response.py
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

In one terminal, start the proxy:

```bash
python3 src/server.py
```

In another terminal, route a request through it:

```bash
curl -x http://localhost:8080 http://example.com/
```

or point an environment variable at it:

```bash
HTTP_PROXY=http://localhost:8080 curl http://example.com/
```

## Example output

```
Proxy server is running on http://localhost:8080
Accepted connection from ('127.0.0.1', 42134)
0 'GET http://example.com/ HTTP/1.1'
1 'Host: example.com'
2 'User-Agent: curl/8.0'
3 'Proxy-Connection: Keep-Alive'
4 ''
Forwarding request to example.com:80
0 'HTTP/1.1 200 OK'
1 'Date: Mon, 03 Aug 2026 12:00:00 GMT'
2 'Content-Length: 1256'
3 'Connection: close'
4 ''
HTTP/1.1 200 OK
```

The proxy logs each forwarded request, the origin it reached, and the parsed
status line of the response.

## Roadmap details

See [docs/roadmap.md](docs/roadmap.md) for the full journey and
[docs/learning-notes.md](docs/learning-notes.md) for the learning journal.

## License

[MIT](LICENSE)
