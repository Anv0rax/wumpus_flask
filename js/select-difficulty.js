// TODO : Essayer de faire en sorte que si on a activé le param FullScreen, Mute ou autre dans le menu Settings, que ces changements soient aussi effectués partout.
document.addEventListener('DOMContentLoaded', () =>
{
    /* ======== Constantes ========*/
    const choice = document.getElementById('difficulty-choice');
    const form = document.getElementById('form');
    const move = document.getElementById('son1');
    const interact = document.getElementById('son2');
    const onoff = document.querySelectorAll('.check');
    const validsound = document.getElementById('son3');

    const lum = document.getElementById('light');
    const sfx = document.getElementById('sfx');
    const music = document.getElementById('music');
    const sound = document.getElementById('sound');

    const checkFs = document.getElementById('checkFs');
    const checkPerf = document.getElementById('checkPerf');

    /* ====================================== */

    choice.addEventListener('change', (el) => {
        const val = choice.value;
        if(val == "ez") choice.style.color = "green";
        if(val == "meh") choice.style.color = "orange";
        if(val == "hard") choice.style.color = "red";
        PlaySound(move);
    });

    onoff.forEach((el) => {
        el.addEventListener('click', () => {
            PlaySound(interact)
        });
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        PlaySound(validsound);
        setTimeout(() => {
            form.submit();
        }, 1000);
    });

        sound.addEventListener('click', () => {
        if(sound.src.includes("SoundWhite.png"))
        {
            sound.src = "../assets/SoundMuteWhite.png";
            move.volume = 0;
            interact.volume = 0;
            validsound.volume = 0;
        }
        else
        {
            sound.src = "../assets/SoundWhite.png";
            move.volume = 0.5;
            interact.volume = 0.5;
            validsound.volume = 0.5;
        }

        /*checkPerf.addEventListener('click', (event) => 
        {
            const testCheck = event.target.checked;
            if(testCheck == true)
            {
                lowPerf.style.setProperty('display', 'none', 'important');
            }
            else
            {
                lowPerf.style.setProperty('display', 'block', 'important');
            }
        });

        checkFs.addEventListener('click', (event) => 
        {
            const testCheck = event.target.checked;
            if(testCheck == true)
            {
                OpenFs();
            }
            else
            {
                CloseFs();
            }
        });*/
    });
});

function PlaySound(el)
{
    el.currentTime = 0;
    el.play();
}

function OpenFs()
{
    if(document.body)
    {
        document.body.requestFullscreen();
    }
    /* sa c'est pour safari */
    else if(document.body.webkitRequestFullscreen)
    {
        document.body.webkitRequestFullscreen();
    }
}

function CloseFs()
{
    if(document.body)
    {
        document.exitFullscreen();
    }
}