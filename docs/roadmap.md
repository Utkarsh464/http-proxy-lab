# Roadmap

This project grows one milestone at a time. Each milestone is only started
when the previous one is understood and committed. Nothing here is
pre-written ahead of time — the repository only ever contains code that
actually exists today.

Legend: `[x]` done · `[ ]` planned

## The journey

```
TCP
  ↓
HTTP Parser
  ↓
Request Object [done]
  ↓
Body Parser [done]
  ↓
Response Parser [done]
  ↓
Forward Proxy [done]
  ↓
Cookie Parser
  ↓
Query Parameter Parser
  ↓
Logger
  ↓
HTTPS CONNECT
  ↓
Thread Pool
  ↓
Persistent Connections
  ↓
HTTP/2
  ↓
Testing
  ↓
Production Ready
```

## Milestones

| # | Milestone | Status | Notes |
|---|-----------|--------|-------|
| 1 | TCP socket server | [x] | Bind, listen, accept, recv |
| 2 | Receive raw HTTP requests | [x] | First bytes over the wire |
| 3 | Decode raw bytes | [x] | `bytes` → `str` (UTF-8) |
| 4 | Parse request line | [x] | Method, path, version |
| 5 | Parse generic headers | [x] | Header: value pairs |
| 6 | Request object | [x] | First-class representation of a request |
| 7 | Body parser | [x] | Extract everything after the blank line |
| 8 | Response parser | [x] | Status line, headers, body |
| 9 | Cookie parser | [ ] | `Cookie` / `Set-Cookie` handling |
| 10 | Query parameter parser | [ ] | Parse `?key=value` pairs from the path |
| 11 | Logger | [ ] | Structured, human-readable request logging |
| 12 | Forward proxy | [x] | Relay requests to origin servers |
| 13 | HTTPS CONNECT | [ ] | Tunnel encrypted traffic |
| 14 | Thread pool | [ ] | Handle multiple clients concurrently |
| 15 | Persistent connections | [ ] | Keep-alive support |
| 16 | HTTP/2 | [ ] | Binary framing, multiplexing |
| 17 | Unit tests | [ ] | Test the parser against real sample requests |
| 18 | Production ready | [ ] | Error handling, hardening, packaging |

## Guiding rules

- **YAGNI** — only build what the current milestone requires.
- **No shortcuts** — no framework drops us in at the top of the ladder.
- **Document while learning** — every milestone updates
  [learning-notes.md](learning-notes.md).
- **Ship what exists** — a milestone is only "done" when its code is
  committed and demonstrated.
