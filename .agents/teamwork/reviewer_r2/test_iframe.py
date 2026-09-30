import http.server
import socketserver
import threading
import functools
import subprocess
import time

# Create test wrapper pages that embed the site in an exact 375px and 320px iframe
for width in [375, 320, 412]:
    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
  margin: 0;
  padding: 0;
  background: #333;
  display: flex;
  justify-content: center;
}}
iframe {{
  width: {width}px;
  height: 1200px;
  border: 2px solid red;
  background: #faf8f4;
}}
</style>
</head>
<body>
<iframe id="test-frame" src="/index.html"></iframe>
</body>
</html>
"""
    with open(f"e:/2026/PersonalWebsite/dist/wrap_{width}.html", "w", encoding="utf-8") as f:
        f.write(wrapper_html)

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=r"e:\2026\PersonalWebsite\dist")
httpd = socketserver.TCPServer(("", 8127), handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for w in [375, 320]:
    out_img = f"e:/2026/PersonalWebsite/.agents/teamwork/reviewer_r2/iframe_{w}.png"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--window-size=800,1400",
        f"--screenshot={out_img}",
        f"http://localhost:8127/wrap_{w}.html"
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"Captured iframe {w}px.")

httpd.shutdown()
