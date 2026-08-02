# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## v0.2.0 (Work In Progress)

Added:
- Request object
- Modular parser
- Cleaner architecture

Changed:
- Parser returns Request object
- Networking and parsing separated

---

## [0.1.0] - 2026-08-02

### Added
- TCP socket server (`src/server.py`) that:
  - Binds to `localhost:8080`
  - Accepts a single connection
  - Receives raw HTTP request bytes
  - Decodes raw bytes as UTF-8
  - Parses the request line (method, path, HTTP version)
  - Parses generic HTTP headers
- Project documentation: `README.md`, `docs/roadmap.md`, `docs/learning-notes.md`
- Sample request test fixture: `tests/sample_requests/basic-get.txt`

### Notes
- Milestone established the foundation. The server was intentionally minimal.
- `recv(1024)` was a known limitation — large HTTP requests would be truncated.
- Only one client could connect at a time.

[0.1.0]: https://github.com/Utkarsh464/http-proxy-lab/releases/tag/v0.1.0
