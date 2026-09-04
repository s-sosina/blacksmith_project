# blacksmith_project

Wearable Telemetry API Service

## Overview
This service processes wearable telemetry data and generates mobility insights.

## Quick Start

### Installation
Creates a local virtual environment (`.venv`) and installs runtime plus dev dependencies. This avoids writing to the system Python, which modern Linux distributions restrict by default.

```bash
make install
```

### Running the Service
```bash
# Default port (8000)
make run

# Custom port
PORT=8080 make run
```

### Health Check
Once the service is running, verify it's healthy:
```bash
curl http://localhost:8000/health
# Expected response: {"status":"ok","service":"blacksmith_project"}
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Running Tests
```bash
make test
```

### Cleaning
```bash
make clean
```

## Configuration
The service can be configured using environment variables:
- `PORT`: The port to bind the service to (default: 8000)

## Error Handling
If the specified port is already in use, the service will exit with a clear error message:
```
Error: Port 8000 is already in use.
Please free up the port or specify a different one using the PORT environment variable.
```