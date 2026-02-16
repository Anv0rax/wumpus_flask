/* =========== Main ================= */

document.addEventListener('DOMContentLoaded', () => 
{
    const containerWelcomeText = document.getElementById('container-texts');
    const spacePressSound = document.getElementById('son');

    function keyPress(event)
    {
        const welcomeText = containerWelcomeText.querySelectorAll('.text');
        welcomeText.forEach(element =>
            {
                element.style.animation = 'none';
                void el.offsetWidth; // Reflox, for the fluidity of the animation blinking.
                element.classList.add('keyPressed');
            }
        )
        setTimeout( () => { playSound(spacePressSound); }, "500");
        setTimeout( () => { fadeOut(containerWelcomeText); }, "500");
    }

    document.addEventListener('keydown', keyPress, {once: true}); // The parameter once : true is to prevent the user to press multiple time his key, making the sound repeat himself.
});

/* =============== Fonctions ============== */

function playSound(el) 
{
    el.currentTime = 0;
    el.volume = 0.5;
    el.play();
}

function fadeOut(el) // The fonction will reduce the opacity of the containerWelcomeText, and when the opacity reach 0 with the help of clearInterval it will stop the container to reduce when the limit is atteigned.
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
