from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            response = '''
            <html>
                <head><title>Python Docker App</title></head>
                <body>
                    <h1>Python Application with Best Practices 🐳</h1>
                    <p>This Docker image demonstrates:</p>
                    <ul>
                        <li>Multi-stage builds</li>
                        <li>Non-root user</li>
                        <li>Health checks</li>
                        <li>Minimal image size</li>
                    </ul>
                    <p><a href="/health">Health Check</a> | <a href="/info">Container Info</a></p>
                </body>
            </html>
            '''
            self.wfile.write(response.encode())
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': 'healthy'})
            self.wfile.write(response.encode())
        
        elif self.path == '/info':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({
                'hostname': os.environ.get('HOSTNAME', 'unknown'),
                'user': os.environ.get('USER', 'unknown'),
                'python_version': os.sys.version,
                'path': os.environ.get('PATH', 'unknown')
            }, indent=2)
            self.wfile.write(response.encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server(8000)
