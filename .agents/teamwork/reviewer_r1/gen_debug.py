with open(r'e:\2026\PersonalWebsite\dist\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

debug_script = """
<pre id="overflow-debug"></pre>
<script>
window.addEventListener('load', () => {
    const out = [];
    const all = document.querySelectorAll('*');
    for (const el of all) {
        const rect = el.getBoundingClientRect();
        if (rect.right > 376) {
            out.push(el.tagName + '.' + (el.className || '').toString().slice(0, 50) + ' -> right: ' + Math.round(rect.right) + ' width: ' + Math.round(rect.width));
        }
    }
    document.getElementById('overflow-debug').textContent = out.join('\\n');
});
</script>
"""

html_debug = html.replace('</body>', debug_script + '</body>')
with open(r'e:\2026\PersonalWebsite\dist\debug.html', 'w', encoding='utf-8') as f:
    f.write(html_debug)
print('Wrote debug.html successfully')
