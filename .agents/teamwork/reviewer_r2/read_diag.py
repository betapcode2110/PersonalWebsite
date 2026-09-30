import re

for w in [375, 320]:
    with open(f"e:/2026/PersonalWebsite/.agents/teamwork/reviewer_r2/dump_{w}.html", "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'<pre id="DIAG_RESULT">(.*?)</pre>', content, re.DOTALL)
    print(f"=== WIDTH {w} ===")
    if m:
        print(m.group(1))
    else:
        print("DIAG_RESULT not found")
