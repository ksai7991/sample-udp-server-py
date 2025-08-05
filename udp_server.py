import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- UDP server setup ---
UDP_IP = "0.0.0.0"
UDP_PORT = 9999

def run_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"✅ UDP server listening on port {UDP_PORT}...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"📩 [UDP] Received from {addr}: {data.decode()}")

# --- HTTP server with /health endpoint ---
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/health", "/sample-udp-server-py"]:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return  # Suppress logs

HTTP_PORT = 8080

def run_http_server():
    server_address = ('', HTTP_PORT)
    httpd = HTTPServer(server_address, HealthHandler)
    print(f"🌐 HTTP server listening on port {HTTP_PORT}...")
    httpd.serve_forever()

# --- TCP echo server setup ---
TCP_IP = "0.0.0.0"
TCP_PORT = 3550

def run_tcp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(5)
    print(f"🔌 TCP server listening on port {TCP_PORT}...")

    while True:
        conn, addr = sock.accept()
        print(f"📥 [TCP] Connection from {addr}")
        data = conn.recv(1024)
        if data:
            print(f"📨 [TCP] Received: {data.decode()}")
            conn.sendall(data)  # Echo back
        conn.close()

# --- Run all servers ---
if __name__ == "__main__":
    udp_thread = threading.Thread(target=run_udp_server, daemon=True)
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    tcp_thread = threading.Thread(target=run_tcp_server, daemon=True)

    udp_thread.start()
    http_thread.start()
    tcp_thread.start()

    udp_thread.join()
    http_thread.join()
    tcp_thread.join()
