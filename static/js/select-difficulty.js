document.addEventListener('DOMContentLoaded', () =>
{
    /* ======== Constantes ========*/

    const checkDifficulty = document.getElementById('difficulty-choice');
    const form = document.getElementById('form');
    const soundOnMove = document.getElementById('son1');
    const interactSound = document.getElementById('son2');
    const checkBouton = document.querySelectorAll('.selectGamemode');
    const validSound = document.getElementById('son3');
    const imageOfSound = document.getElementById('soundImage');
    

    /* ====================================== */

    checkDifficulty.addEventListener('change', (el) => {
        const val = checkDifficulty.value;
        if(val == "easy") checkDifficulty.style.color = "green";
        if(val == "medium") checkDifficulty.style.color = "orange";
        if(val == "hard") checkDifficulty.style.color = "red";
        PlaySound(soundOnMove);
    });

    checkBouton.forEach((el) => {             
        el.addEventListener('click', () => {
            PlaySound(interactSound)
        });
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        PlaySound(validSound);
        setTimeout(() => {
            form.submit();
        }, 1000);
    });

        imageOfSound.addEventListener('click', () => {
        if(imageOfSound.src.includes("SoundWhite.png"))
        {
            imageOfSound.src = "../static/assets/SoundMuteWhite.png";
            soundOnMove.volume = 0;
            interactSound.volume = 0;
            validSound.volume = 0;
        }
        else
        {
            imageOfSound.src = "../static/assets/SoundWhite.png";
            soundOnMove.volume = 0.5;
            interactSound.volume = 0.5;
            validSound.volume = 0.5;
        }
    });
});

function PlaySound(el)
{
    el.currentTime = 0;
    el.play();
}