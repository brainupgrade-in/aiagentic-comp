#!/usr/bin/env python3
"""
Dashboard server — serves the HTML dashboard and handles refresh requests.

Usage:
    python3 reporting/server.py
    Open: http://localhost:8888
"""

import http.server
import subprocess
import json
import os
import re

PORT = 8888
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_PATH = os.path.join(BASE_DIR, "reporting", "dashboard.html")
SCRIPT_PATH = os.path.join(BASE_DIR, "reporting", "generate-dashboard.py")
TOKEN_FILE = os.path.expanduser("~/.rajesh/.github_bu")
SINCE = os.getenv("DASHBOARD_SINCE")  # YYYY-MM-DD; scopes the dashboard to one cohort


class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/dashboard.html"):
            self.serve_file(DASHBOARD_PATH, "text/html")
        elif self.path == "/refresh":
            self.run_refresh(session=None)
        elif m := re.match(r"^/refresh/session/(\d+)$", self.path):
            self.run_refresh(session=int(m.group(1)))
        else:
            self.send_error(404)

    def run_refresh(self, session):
        cmd = ["python3", SCRIPT_PATH, "--output", DASHBOARD_PATH]
        if session:
            cmd += ["--session", str(session)]
        if SINCE:
            cmd += ["--since", SINCE]

        env = os.environ.copy()
        if not env.get("GITHUB_TOKEN") and os.path.exists(TOKEN_FILE):
            env["GITHUB_TOKEN"] = open(TOKEN_FILE).read().strip()

        label = f"session {session}" if session else "all sessions"
        print(f"  Refreshing {label}...", flush=True)
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=env, cwd=BASE_DIR
        )

        self.send_response(200 if result.returncode == 0 else 500)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if result.returncode == 0:
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.wfile.write(
                json.dumps({"status": "error", "message": result.stderr}).encode()
            )

    def serve_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type + "; charset=utf-8")
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

    def log_message(self, fmt, *args):
        pass  # suppress default per-request logging


if __name__ == "__main__":
    server = http.server.HTTPServer(("localhost", PORT), DashboardHandler)
    print(f"Dashboard server → http://localhost:{PORT}")
    if SINCE:
        print(f"Counting submissions from {SINCE} onward.")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
