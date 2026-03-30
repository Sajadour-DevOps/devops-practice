from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <body>
        <h1>Hello from Python App!</h1>
        <p>Running on port 5000</p>
        <p>Proxied through nginx</p>
        </body>
        </html>
        """)

    def log_message(self, format, *args):
        pass

print("Python app running on port 5000...")
HTTPServer(('0.0.0.0', 5000), Handler).serve_forever()
