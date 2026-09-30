import http.server
import socketserver
import threading
import functools
import subprocess
import time
import os

PORT = 8130
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=r"e:\2026\PersonalWebsite\dist")
httpd = socketserver.TCPServer(("", PORT), handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
out_dir = r"e:\2026\PersonalWebsite\.agents\teamwork\reviewer_r2"

# 1. Desktop test (1024x1600)
cmd1 = [
    edge_path,
    "--headless=new",
    "--disable-gpu",
    "--virtual-time-budget=2000",
    "--window-size=1024,1800",
    f"--screenshot={out_dir}\\desktop_vtime.png",
    f"http://localhost:{PORT}/index.html"
]
subprocess.run(cmd1)

# 2. Also take mobile with virtual time budget
cmd2 = [
    edge_path,
    "--headless=new",
    "--disable-gpu",
    "--virtual-time-budget=2000",
    "--window-size=600,1800",
    f"--screenshot={out_dir}\\view_600.png",
    f"http://localhost:{PORT}/index.html"
]
subprocess.run(cmd2)

print("Desktop screenshot done.")
httpd.shutdown()
