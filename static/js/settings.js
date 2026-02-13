// TODO : Faire en sorte que le son ne soit dépendant que des sliders, et non du code
// TODO : Essayer de faire le lien entre la page du choix de la difficulté, et que la aussi le son par exemple de la musique soit la même dans le menu paramétres ou dans le menu choix difficulté.
// TODO : Régler les sliders, leur css.

document.addEventListener('DOMContentLoaded', () => {

    /* ========= Les constantes ==========*/
    const move = document.getElementById('son1');
    const interact = document.getElementById('son2');
    const lowPerf = document.getElementById('deco');
    const onoff = document.querySelectorAll('.check');
    const test = document.getElementById('test');
    const sliderSound = document.getElementById('son4');
    const testMusicPrincipal = document.getElementById('mario');

    const lum = document.getElementById('light');
    const sfx = document.getElementById('sfx');
    const music = document.getElementById('music');
    const sound = document.getElementById('sound');
    const pLum = document.getElementById('pLum');
    const pSfx = document.getElementById('pSfx');
    const pMusic = document.getElementById('pMusic');

    const checkFs = document.getElementById('checkFs');
    const checkPerf = document.getElementById('checkPerf');

    /* =========================================== */

    /* ======== Le Code ========== */

    let musicVolume = 0.25;
    let soundVolume = 0.25;
    testMusicPrincipal.volume = 0.05;
    sliderSound.volume = 0.25;
    pLum.textContent = "100%";
    pSfx.textContent = sfx.value + "%";
    pMusic.textContent = music.value + "%";

    onoff.forEach((el) => {
        el.addEventListener('click', () => {
            PlaySound(interact)
        });
    });

    sound.addEventListener('click', () => {
        if(sound.src.includes("SoundWhite.png"))
        {
            sound.src = "../static/assets/SoundMuteWhite.png";
            move.volume = 0;
            interact.volume = 0;
            sliderSound.volume = 0;
            sfx.value = 0;
            music.value = 0;
            pSfx.textContent = "Mute activé !";
            pMusic.textContent = "Mute activé !";
            DisableSlider(sfx);
            DisableSlider(music);
            SongVolume(testMusicPrincipal, music.value);
        }
        else
        {
            sound.src = "../static/assets/SoundWhite.png";
            EnableSlider(sfx);
            EnableSlider(music);
            move.volume = soundVolume;
            interact.volume = soundVolume;
            sliderSound.volume = soundVolume;
            sfx.value = soundVolume*100;
            music.value = musicVolume*100;
            SongVolume(testMusicPrincipal, musicVolume)
            pSfx.textContent = sfx.value + "%";
            pMusic.textContent = music.value + "%";
        }
    });

    lum.addEventListener('input', () => {
        PlaySound(sliderSound);
        UpdateBrightness(lum);
        pLum.textContent = lum.value  + "%";
    });

    sfx.addEventListener('input', () => {
        PlaySound(sliderSound);
        var val = sfx.value / 100;
        move.volume = val;
        interact.volume = val;
        sliderSound.volume = val;
        soundVolume = val;
        pSfx.textContent = sfx.value + "%";
    });

    music.addEventListener('input', () => 
    {
        PlaySound(sliderSound);
        var val = music.value / 100;
        musicVolume = val;
        SongVolume(testMusicPrincipal, val);
        pMusic.textContent = music.value + "%";
    });

    checkPerf.addEventListener('click', (event) => 
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
    });

    /* ================================================== */

});

    /* ================= Fonctions ==================== */

function PlaySound(el)
{
    el.currentTime = 0;
    el.play();
}

function UpdateBrightness(slider) 
{
    const val = slider.value;
    ApplyBrightnessToGame(val / 100);
}

function ApplyBrightnessToGame(level) 
{
    document.body.style.filter = `brightness(${level})`;
}

function DisableSlider(el)
{
    el.disabled = true;
}

function EnableSlider(el)
{
    el.disabled = false;
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

function SongVolume(song, volumeSong)
{
    song.volume = volumeSong;
}

    /* ===================================== */
