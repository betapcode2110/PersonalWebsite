with open(r"e:\2026\PersonalWebsite\dist\index.html", "r", encoding="utf-8") as f:
    html = f.read()

no_anim_style = "<style>*, *::before, *::after { animation: none !important; opacity: 1 !important; }</style>"
html_settled = html.replace("</head>", no_anim_style + "</head>")

with open(r"e:\2026\PersonalWebsite\dist\settled.html", "w", encoding="utf-8") as f:
    f.write(html_settled)

for w in [375, 320]:
    wrap_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
  margin: 0;
  padding: 0;
  background: #111;
  display: flex;
  justify-content: center;
}}
iframe {{
  width: {w}px;
  height: 2000px;
  border: 1px solid #ff00ff;
  background: #faf8f4;
}}
</style>
</head>
<body>
<iframe src="/settled.html" scrolling="no"></iframe>
</body>
</html>"""
    with open(f"e:/2026/PersonalWebsite/dist/wrap_{w}_settled.html", "w", encoding="utf-8") as f:
        f.write(wrap_html)

print("Generated settled test files.")
