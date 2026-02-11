console.log("script title chargé !");
document.addEventListener('DOMContentLoaded', () => 
{
    const title = document.getElementById('container-texts');
    const select = document.getElementById('son');

    function keyPress(event)
    {
        const test = title.querySelectorAll('.text');
        test.forEach(el =>
            {
                el.style.animation = 'none';
                void el.offsetWidth; // un Reflow pour que les animations des deux textes se jouent en même temps
                el.classList.add('keyPressed');
            }
        )
        setTimeout( () => { playSound(select); }, "500");
        setTimeout( () => { fadeOut(title); }, "500");
    }

    document.addEventListener('keydown', keyPress, {once: true}); // once true permet que l'event ne se fait qu'une seule fois, pour éviter le spam aprés
});

function playSound(el)
{
    el.currentTime = 0;
    el.volume = 0.5;
    el.play();
}

function fadeOut(el) // la fonction va réduire de 0.05 d'opacité a chaque 100 milisecondes. Quand l'opacité atteint est en dessous de 0, il va arrêter la boucle grâce a clearInterval.
{
    var opacity = 1;
    var timer = setInterval(function () {
        if(opacity < 0)
        {
            clearInterval(timer);
        }
        el.style.opacity = opacity;
        el.style.filter = 'alpha(opacity = ' + opacity + 10 + ")";
        opacity -= 0.05;
    }, 100);
}
