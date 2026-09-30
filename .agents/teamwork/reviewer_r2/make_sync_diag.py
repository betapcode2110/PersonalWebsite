import re

# We modify dist/index.html to write out the widths directly into a visible div during page load
with open(r"e:\2026\PersonalWebsite\dist\index.html", "r", encoding="utf-8") as f:
    html = f.read()

script = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    const lines = [];
    lines.push('win.innerWidth=' + window.innerWidth);
    lines.push('doc.clientWidth=' + document.documentElement.clientWidth);
    lines.push('doc.scrollWidth=' + document.documentElement.scrollWidth);
    lines.push('body.clientWidth=' + document.body.clientWidth);
    lines.push('body.scrollWidth=' + document.body.scrollWidth);
    
    // Find all elements wider than window.innerWidth
    document.querySelectorAll('*').forEach(el => {
        if (el.scrollWidth > window.innerWidth || el.offsetWidth > window.innerWidth) {
            lines.push('OVERFLOW: ' + el.tagName + '.' + (el.className || '') + ' sw=' + el.scrollWidth + ' ow=' + el.offsetWidth);
        }
    });

    const box = document.createElement('pre');
    box.id = 'VISIBLE_DIAG';
    box.style.background = 'yellow';
    box.style.color = 'black';
    box.style.fontSize = '12px';
    box.style.padding = '10px';
    box.textContent = lines.join('\\n');
    document.body.insertBefore(box, document.body.firstChild);
});
</script>
"""

with open(r"e:\2026\PersonalWebsite\dist\diag_sync.html", "w", encoding="utf-8") as f:
    f.write(html.replace("<body", script + "<body"))

print("Created diag_sync.html")
