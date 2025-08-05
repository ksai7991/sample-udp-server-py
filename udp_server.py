import socket
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# --- UDP server setup ---
UDP_IP = "0.0.0.0"
UDP_PORT = 9999

def run_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"✅ UDP server listening on port {UDP_PORT}...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"📩 Received message from {addr}: {data.decode()}")

# --- HTTP server setup ---
HTTP_PORT = 8080

def run_http_server():
    server_address = ('', HTTP_PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"🌐 HTTP server listening on port {HTTP_PORT}...")
    httpd.serve_forever()

# --- Run both servers ---
if __name__ == "__main__":
    udp_thread = threading.Thread(target=run_udp_server, daemon=True)
    http_thread = threading.Thread(target=run_http_server, daemon=True)

    udp_thread.start()
    http_thread.start()

    # Keep the main thread alive
    udp_thread.join()
    http_thread.join()
