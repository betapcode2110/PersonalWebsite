import http.server
import socketserver
import threading
import functools
import subprocess
import re

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=r"e:\2026\PersonalWebsite\dist")
httpd = socketserver.TCPServer(("", 8126), handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for w in [375, 320]:
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--window-size={w},1800",
        "--dump-dom",
        "http://localhost:8126/diag_sync.html"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    m = re.search(r'<pre id="VISIBLE_DIAG"[^>]*>(.*?)</pre>', res.stdout, re.DOTALL)
    print(f"=== VIEWPORT {w} ===")
    if m:
        print(m.group(1))
    else:
        print("VISIBLE_DIAG not found")

httpd.shutdown()
