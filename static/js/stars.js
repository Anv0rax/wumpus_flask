document.addEventListener("DOMContentLoaded", function()
{
    const starsContainer = document.getElementById('stars');

    for (let i = 0; i < 120; i++)
    {
        const star = document.createElement('div');
        star.classList.add('star');
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.setProperty('--dur', (2 + Math.random() * 4) + 's');
        star.style.setProperty('--delay', (Math.random() * 4) + 's');
        star.style.setProperty('--opacity', (0.4 + Math.random() * 0.6).toString());
        star.style.width = (Math.random() > 0.8 ? 3 : 2) + 'px';
        star.style.height = star.style.width;
        starsContainer.appendChild(star);
    }
});
