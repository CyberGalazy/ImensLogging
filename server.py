"""
PC Logging Server
Runs on your laptop to receive logs from all gaming zone PCs
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
from typing import Dict

from pc_logger import PCLogger


class LoggingServerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for receiving PC logs"""
    
    def __init__(self, logger: PCLogger, *args, **kwargs):
        self.logger = logger
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """Override to customize log format"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")
    
    def do_GET(self):
        """Handle GET requests - return current logs or PC info"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/status':
            # Return server status
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "running", "message": "PC Logging Server is active"}
            self.wfile.write(json.dumps(response).encode())
        
        elif path == '/logs':
            # Return all logs
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(self.logger.logs, indent=2).encode())
        
        elif path.startswith('/pc/'):
            # Return specific PC info
            pc_name = path.split('/pc/')[1]
            pc_info = self.logger.get_pc_info(pc_name)
            
            self.send_response(200 if pc_info else 404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if pc_info:
                self.wfile.write(json.dumps(pc_info, indent=2).encode())
            else:
                self.wfile.write(json.dumps({"error": "PC not found"}).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def do_POST(self):
        """Handle POST requests - receive logs from clients"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/log':
            # Receive log data from client
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                pc_name = data.get('pc_name')
                status = data.get('status', 'running')
                software = data.get('software', [])
                
                if not pc_name:
                    raise ValueError("pc_name is required")
                
                # Log the data
                self.logger.log_pc_with_software(pc_name, software, status)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"status": "success", "message": f"Logged data for {pc_name}"}
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                # Send error response
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def create_handler(logger):
    """Factory function to create handler with logger instance"""
    def handler(*args, **kwargs):
        return LoggingServerHandler(logger, *args, **kwargs)
    return handler


class LoggingServer:
    """Main server class"""
    
    def __init__(self, host='0.0.0.0', port=8080, log_file='pc_logs.json'):
        """
        Initialize the logging server.
        
        Args:
            host: Host address to bind to (0.0.0.0 for all interfaces)
            port: Port number to listen on
            log_file: Path to JSON file for storing logs
        """
        self.host = host
        self.port = port
        self.logger = PCLogger(log_file)
        self.server = None
        self.server_thread = None
    
    def start(self):
        """Start the HTTP server"""
        handler = create_handler(self.logger)
        self.server = HTTPServer((self.host, self.port), handler)
        
        print("="*60)
        print("PC LOGGING SERVER")
        print("="*60)
        print(f"Server running on http://{self.host}:{self.port}")
        print(f"Waiting for logs from gaming zone PCs...")
        print(f"Press Ctrl+C to stop the server")
        print("="*60)
        print()
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            self.stop()
    
    def stop(self):
        """Stop the HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Server stopped.")
    
    def start_background(self):
        """Start server in background thread"""
        self.server_thread = threading.Thread(target=self.start, daemon=True)
        self.server_thread.start()
        return self.server_thread


if __name__ == "__main__":
    import sys
    
    # Get configuration from command line or use defaults
    host = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    
    server = LoggingServer(host=host, port=port)
    server.start()

