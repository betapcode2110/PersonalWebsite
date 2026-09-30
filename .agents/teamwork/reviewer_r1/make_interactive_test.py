with open(r'e:\2026\PersonalWebsite\dist\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

test_script = """
<script>
window.addEventListener('load', () => {
    setTimeout(() => {
        try {
            const tabs = document.querySelectorAll('.tab-btn');
            const notes = document.querySelectorAll('.note-item');
            
            console.log('Total tabs:', tabs.length, 'Total notes:', notes.length);
            if (tabs.length < 4 || notes.length < 5) throw new Error('Tabs or notes missing');
            
            // Initial state: 'all' is active
            const allTab = document.querySelector('[data-category="all"]');
            if (!allTab.classList.contains('tab-active') || !allTab.classList.contains('bg-black')) {
                throw new Error('Initial active tab does not have tab-active/bg-black');
            }
            
            // 1. Click 'Tech Art' tab
            const techArtTab = document.querySelector('[data-category="Tech Art"]');
            if (!techArtTab) throw new Error('Tech Art tab not found');
            techArtTab.click();
            
            if (!techArtTab.classList.contains('tab-active') || !techArtTab.classList.contains('bg-black')) {
                throw new Error('Tech Art tab active classes missing after click');
            }
            if (allTab.classList.contains('tab-active') || allTab.classList.contains('bg-black')) {
                throw new Error('all tab still has active classes after Tech Art clicked');
            }
            
            // Check note visibility
            notes.forEach(note => {
                const tag = note.getAttribute('data-tag');
                if (tag === 'Tech Art') {
                    if (note.style.display !== '') throw new Error('Tech Art note hidden when it should be visible');
                } else {
                    if (note.style.display !== 'none') throw new Error('Non-Tech Art note visible when it should be hidden: ' + tag);
                }
            });
            
            // 2. Click 'Shader' tab
            const shaderTab = document.querySelector('[data-category="Shader"]');
            shaderTab.click();
            if (!shaderTab.classList.contains('tab-active')) throw new Error('Shader tab not active');
            notes.forEach(note => {
                const tag = note.getAttribute('data-tag');
                if (tag === 'Shader') {
                    if (note.style.display !== '') throw new Error('Shader note hidden');
                } else {
                    if (note.style.display !== 'none') throw new Error('Non-Shader note visible');
                }
            });
            
            // 3. Click 'all' tab again
            allTab.click();
            if (!allTab.classList.contains('tab-active')) throw new Error('all tab not active after click');
            notes.forEach(note => {
                if (note.style.display !== '') throw new Error('Note still hidden after all clicked');
            });
            
            document.title = 'INTERACTIVE_TEST_SUCCESS';
        } catch (e) {
            document.title = 'INTERACTIVE_TEST_FAIL: ' + e.message;
        }
    }, 200);
});
</script>
"""

html_test = html.replace('</body>', test_script + '</body>')
with open(r'e:\2026\PersonalWebsite\dist\test_interactive.html', 'w', encoding='utf-8') as f:
    f.write(html_test)
print('Wrote test_interactive.html')
