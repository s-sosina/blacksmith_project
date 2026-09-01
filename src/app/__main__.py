"""
Entry point for the blacksmith service.
"""
import os
import socket
import sys
import uvicorn
from src.app.main import app

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

def is_port_available(port: int) -> bool:
    """Check if a port is available for binding."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False

def main() -> None:
    """Main entry point for the service."""
    port = get_port()
    
    if not is_port_available(port):
        print(f"Error: Port {port} is already in use.")
        print("Please free up the port or specify a different one using the PORT environment variable.")
        sys.exit(1)
    
    print(f"Starting blacksmith service on port {port}...")
    print(f"Health check available at: http://localhost:{port}/health")
    print(f"API documentation available at: http://localhost:{port}/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()