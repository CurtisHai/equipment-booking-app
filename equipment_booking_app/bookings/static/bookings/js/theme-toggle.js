document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('theme-toggle');
    const body = document.body;

    function setTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            body.classList.remove('light-mode');
            toggle.textContent = '☀';
        } else {
            body.classList.add('light-mode');
            body.classList.remove('dark-mode');
            toggle.textContent = '🌙';
        }
        localStorage.setItem('theme', theme);
    }

    toggle.addEventListener('click', function () {
        const newTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';
        setTheme(newTheme);
    });

    const saved = localStorage.getItem('theme') || 'light';
    setTheme(saved);
});
