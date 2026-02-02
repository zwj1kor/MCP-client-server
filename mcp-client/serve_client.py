"""Simple HTTP server to serve the client on port 8000"""
import http.server
import socketserver
import os

# f

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"  Frontend Server Running")
        print(f"  URL: http://localhost:{PORT}")
        print(f"  Directory: {DIRECTORY}")
        print(f"{'='*60}\n")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()
