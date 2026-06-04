"""Lightweight HTTP server to keep the bot alive on Hugging Face Spaces / Render"""

import http.server
import socketserver
import threading
import os


class KeepAliveHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Arrodes is alive and running!")

    def log_message(self, format, *args):
        # Override to suppress standard HTTP logging and keep console output clean
        pass


def run_server(port):
    # Enable address reuse so restarting the bot does not raise Address-Already-In-Use errors
    socketserver.TCPServer.allow_reuse_address = True
    handler = KeepAliveHandler
    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"📡 Keep-alive server listening on port {port} (ready for health checks)")
        httpd.serve_forever()


def start_keep_alive():
    # Hugging Face Spaces defaults to port 7860, but allow environment override (e.g. PORT)
    port = int(os.getenv("PORT", 7860))
    t = threading.Thread(target=run_server, args=(port,), daemon=True)
    t.start()
