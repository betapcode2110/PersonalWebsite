import http.server
import socketserver
import threading
import functools
import subprocess
import time

PORT = 8135
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=r"e:\2026\PersonalWebsite\dist")
httpd = socketserver.TCPServer(("", PORT), handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
out_dir = r"e:\2026\PersonalWebsite\.agents\teamwork\reviewer_r2"

for w in [1024, 375, 320]:
    wrap_file = f"/wrap_{w}_settled.html" if w != 1024 else "/settled.html"
    win_w = 1040 if w == 1024 else 600
    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={win_w},2200",
        f"--screenshot={out_dir}\\new_{w}.png",
        f"http://localhost:{PORT}{wrap_file}"
    ]
    subprocess.run(cmd)
    print(f"Captured new_{w}.png")

httpd.shutdown()
