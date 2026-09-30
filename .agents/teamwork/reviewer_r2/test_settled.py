import http.server
import socketserver
import threading
import functools
import subprocess

for width in [1024, 375, 320]:
    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
  margin: 0;
  padding: 0;
  background: #222;
  display: flex;
  justify-content: center;
}}
iframe {{
  width: {width}px;
  height: 2200px;
  border: 2px solid lime;
  background: #faf8f4;
}}
</style>
</head>
<body>
<iframe id="test-frame" src="/index.html"></iframe>
<script>
const frame = document.getElementById('test-frame');
frame.addEventListener('load', () => {{
    setTimeout(() => {{
        try {{
            const doc = frame.contentDocument;
            const style = doc.createElement('style');
            style.textContent = `
              *, *::before, *::after {{
                animation-delay: 0s !important;
                animation-duration: 0.001s !important;
                opacity: 1 !important;
                transition-duration: 0.001s !important;
              }}
            `;
            doc.head.appendChild(style);
        }} catch(e) {{}}
    }}, 100);
}});
</script>
</body>
</html>
"""
    with open(f"e:/2026/PersonalWebsite/dist/anim_{width}.html", "w", encoding="utf-8") as f:
        f.write(wrapper_html)

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=r"e:\2026\PersonalWebsite\dist")
httpd = socketserver.TCPServer(("", 8128), handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for w in [1024, 375, 320]:
    out_img = f"e:/2026/PersonalWebsite/.agents/teamwork/reviewer_r2/rendered_{w}.png"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--window-size={max(w + 50, 600)},2400",
        f"--screenshot={out_img}",
        f"http://localhost:8128/anim_{w}.html"
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"Captured rendered {w}px.")

httpd.shutdown()
