with open(r'e:\2026\PersonalWebsite\dist\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'class="([^"]*)"', html)
for m in sorted(set(matches)):
    for token in m.split():
        if token.startswith(('w-', 'min-w-', 'max-w-', 'px-', 'pl-', 'pr-')):
            print(f'{token:20} in class: {m}')
