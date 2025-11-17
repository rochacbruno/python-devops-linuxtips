# Hello API

A simple FastAPI application that provides greeting endpoints with request history tracking.

## Installation

```bash
uv sync
```

## Running

```bash
uv run poe api
```

The API will be available at http://127.0.0.1:8000

## Endpoints

- `GET /hello` - Returns "Hello World"
- `GET /hello/{word}` - Returns greeting with formatted word
- `GET /history` - Returns request history (requires Basic Auth: admin/Batata123)

## Development Tasks

Available poe tasks:

```bash
uv run poe test          # Run tests
uv run poe test-cov      # Run tests with coverage
uv run poe format        # Format code with ruff
uv run poe lint          # Lint code with ruff
uv run poe lint-fix      # Lint and auto-fix issues
uv run poe check         # Run format, lint, and test
uv run poe api           # Run the API with reload
```

## Testing

```bash
curl http://localhost:8000/hello
curl http://localhost:8000/hello/python
curl -u admin:Batata123 http://localhost:8000/history
```
