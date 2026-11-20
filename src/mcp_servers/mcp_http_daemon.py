#!/usr/bin/env python3
import sys
import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

MCP_NAME = sys.argv[1] if len(sys.argv) > 1 else "mcp-aiops"
MCP_SCRIPT = sys.argv[2] if len(sys.argv) > 2 else "/home/hpe/mcp-aiops/src/server.py"
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 8104

class MCPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        out = subprocess.run(["/usr/bin/python3", MCP_SCRIPT, "--test"], capture_output=True, text=True, timeout=15).stdout
        body = json.dumps({"mcp_server": MCP_NAME, "port": PORT, "status": "ACTIVE", "self_test_output": out}, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(length).decode() if length > 0 else '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
        p = subprocess.Popen(["/usr/bin/python3", MCP_SCRIPT, "--stdio"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        out, _ = p.communicate(payload + "\n", timeout=15)
        body = out.encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    srv = HTTPServer(("0.0.0.0", PORT), MCPHandler)
    print(f"[*] {MCP_NAME} JSON-RPC / HTTP MCP Server listening on 0.0.0.0:{PORT}")
    srv.serve_forever()
