document.addEventListener("DOMContentLoaded", () => {
    const colors = [
        'rgba(64,200,224,VAL)',
        'rgba(255,190,77,VAL)',
        'rgba(77,122,255,VAL)',
        'rgba(176,96,255,VAL)',
        'rgba(255,255,255,VAL)',
    ];
    for (let i = 0; i < 30; i++) {
        const dot = document.createElement('div');
        dot.classList.add('pulse-dot');
        const size = 20 + Math.random() * 120;
        const color = colors[i % colors.length].replace('VAL', (0.12 + Math.random() * 0.18).toFixed(2));
        dot.style.width  = size + 'px';
        dot.style.height = size + 'px';
        dot.style.left   = Math.random() * 100 + '%';
        dot.style.top    = Math.random() * 100 + '%';
        dot.style.background = `radial-gradient(circle, ${color}, transparent 70%)`;
        dot.style.setProperty('--dur',   (2.5 + Math.random() * 4) + 's');
        dot.style.setProperty('--delay', (Math.random() * 6) + 's');
        document.querySelector('main').appendChild(dot);
    }
});
