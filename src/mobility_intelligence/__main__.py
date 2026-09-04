"""
Entry point for the blacksmith service.
"""
import os
import socket
import sys
import uvicorn
from mobility_intelligence.main import app

def get_port() -> int:
    """Get port from environment variable with default fallback."""
    try:
        port_str = os.environ.get("PORT", "8000")
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError(f"Port {port} is out of valid range (1-65535)")
        return port
    except ValueError as e:
        print(f"Error: Invalid PORT value '{os.environ.get('PORT')}': {e}")
        print("PORT must be an integer between 1 and 65535")
        sys.exit(1)

def bind_socket(port: int) -> socket.socket:
    """Bind the service port once; fail with a clear message if unavailable."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("0.0.0.0", port))
    except OSError:
        print(f"Error: Port {port} is already in use.")
        print("Please free up the port or specify a different one using the PORT environment variable.")
        sys.exit(1)
    return sock

def main() -> None:
    """Main entry point for the service."""
    port = get_port()

    print(f"Starting blacksmith service on port {port}...")
    print(f"Health check available at: http://localhost:{port}/health")
    print(f"API documentation available at: http://localhost:{port}/docs")

    sock = bind_socket(port)
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run(sockets=[sock])

if __name__ == "__main__":
    main()
