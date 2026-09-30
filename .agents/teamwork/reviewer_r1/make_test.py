with open(r'e:\2026\PersonalWebsite\dist\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

test_script = """
<div id="results" style="display:none;"></div>
<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        const docWidth = document.documentElement.scrollWidth;
        const winWidth = window.innerWidth;
        const elements = document.querySelectorAll('*');
        const overflowing = [];
        for (const el of elements) {
            const r = el.getBoundingClientRect();
            if (r.right > winWidth) {
                overflowing.push(el.tagName + '.' + (el.className || '').slice(0, 30) + ' (right=' + Math.round(r.right) + ', w=' + Math.round(r.width) + ')');
            }
        }
        document.title = 'RESULT: doc=' + docWidth + ' win=' + winWidth + ' bad=' + overflowing.length;
        console.log('RESULT:', document.title, overflowing);
    }, 500);
});
</script>
"""

html_test = html.replace('</head>', test_script + '</head>')
with open(r'e:\2026\PersonalWebsite\dist\test_overflow.html', 'w', encoding='utf-8') as f:
    f.write(html_test)
print('Wrote test_overflow.html')
