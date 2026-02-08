document.addEventListener('DOMContentLoaded', () => {
    const choice = document.getElementById('difficulty-choice');
    const form = document.getElementById('form')
    const move = document.getElementById('son1');
    const interact = document.getElementById('son2');
    const onoff = document.querySelectorAll('.check');
    const test = document.getElementById('test');
    const validsound = document.getElementById('son3');
    const mute = document.getElementById('sound');

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
            move.volume = 1;
            interact.volume = 1;
            validsound.volume = 1;
        }
    });

});

function PlaySound(el)
{
    el.currentTime = 0;
    el.play();
}