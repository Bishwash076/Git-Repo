from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 8000

handler = SimpleHTTPRequestHandler
httpd = HTTPServer(("", PORT), handler)

print(f"Server running on http://localhost:{PORT}")
httpd.serve_forever()
