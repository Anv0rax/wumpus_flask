document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("table tr");
    const table = document.getElementById('table');
    const soundHoverRow = document.getElementById('soundTableAnimation')

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


    rows.forEach((row, index) => {
        row.animate(
            [
                { opacity: 0, transform: "translateY(20px)" },
                { opacity: 1, transform: "translateY(0)" }
            ],
            {
                duration: 500,
                fill: "forwards",
                easing: "ease-out",
                delay: index * 100
            }
        );
    });

    rows.forEach(row => {
        row.addEventListener("mouseenter", () => {
            // Si le son est déjà en train de jouer, on le remet à 0
            soundHoverRow.currentTime = 0;
            // On joue le son
            soundHoverRow.play().catch(e => {
                console.log("Lecture audio bloquée par le navigateur (il faut une interaction avant)");
            });
        });
    });
});
