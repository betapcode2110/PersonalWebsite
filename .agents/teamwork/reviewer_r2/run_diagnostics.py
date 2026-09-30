import http.server
import socketserver
import threading
import subprocess
import time
import os
import sys

import functools

PORT = 8124
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=r"e:\2026\PersonalWebsite\dist")

# Start HTTP server in background thread
httpd = socketserver.TCPServer(("", PORT), handler)
t = threading.Thread(target=httpd.serve_forever)
t.daemon = True
t.start()

time.sleep(1)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# We create an inspect.html in dist with diagnostic script
with open(r"e:\2026\PersonalWebsite\dist\index.html", "r", encoding="utf-8") as f:
    html = f.read()

diag_script = """
<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        const docW = document.documentElement.scrollWidth;
        const winW = window.innerWidth;
        const bodyW = document.body.scrollWidth;
        const out = [];
        document.querySelectorAll('*').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.right > winW + 1) {
                out.push({
                    tag: el.tagName,
                    cls: el.className,
                    right: r.right,
                    width: r.width,
                    text: el.innerText ? el.innerText.slice(0, 30) : ''
                });
            }
        });
        const resDiv = document.createElement('pre');
        resDiv.id = 'DIAG_RESULT';
        resDiv.textContent = JSON.stringify({docW, winW, bodyW, overflowCount: out.length, items: out}, null, 2);
        document.body.appendChild(resDiv);
    }, 500);
});
</script>
"""

with open(r"e:\2026\PersonalWebsite\dist\diag.html", "w", encoding="utf-8") as f:
    f.write(html.replace("</body>", diag_script + "</body>"))

for width in [375, 320]:
    out_img = f"e:/2026/PersonalWebsite/.agents/teamwork/reviewer_r2/test_{width}.png"
    out_html = f"e:/2026/PersonalWebsite/.agents/teamwork/reviewer_r2/dump_{width}.html"
    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={width},1800",
        f"--screenshot={out_img}",
        f"--dump-dom",
        f"http://localhost:{PORT}/diag.html"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(res.stdout)
    print(f"Captured {width}px.")

httpd.shutdown()
