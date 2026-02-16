// TODO : Essayer de faire le lien entre la page du choix de la difficulté, et que la aussi le son par exemple de la musique soit la même dans le menu paramétres ou dans le menu choix difficulté.
// TODO : Régler les sliders, leur css.

document.addEventListener('DOMContentLoaded', () => {

    /* ========= the const ==========*/
    const soundOnMove = document.getElementById('son1');
    const interactSound = document.getElementById('son2');
    const lowPerformanceMode = document.getElementById('backgroundAnimationRings');
    const checkBouton = document.querySelectorAll('.check'); 
    const sliderSound = document.getElementById('son4');
    const mainMusic = document.getElementById('mario');

    const luminosity = document.getElementById('light');
    const sfx = document.getElementById('sfx');
    const volumeValueOfmusic = document.getElementById('music');
    const imageOfSound = document.getElementById('sound');
    const paragraphLum = document.getElementById('pLum');
    const paragraphSfx = document.getElementById('pSfx');
    const paragraphMusic = document.getElementById('pMusic');

    const checkFullScreen = document.getElementById('checkFs');
    const checkPerformanceMode = document.getElementById('checkPerf');

    const sliders = document.querySelectorAll('.slider');

    /* =========================================== */

    /* ======== the code ========== */

    let musicVolume = 0.05;
    let soundVolume = 0.25;
    mainMusic.volume = musicVolume;
    sliderSound.volume = soundVolume;

    window.addEventListener('mousedown', () => 
    {
        if (mainMusic.paused) 
        {
            mainMusic.play();
        }
    }, { once: true }); // Because of the Security rules put by Chrome, safari, etc... I'm obliged to force the user to click on the page, because chrome is denying it.

    paragraphLum.textContent = luminosity.value + '%';
    paragraphSfx.textContent = sfx.value + "%";
    paragraphMusic.textContent = volumeValueOfmusic.value + "%";

    checkBouton.forEach((el) => {
        el.addEventListener('click', () => {
            PlaySound(interactSound)
        });
    });

    sliders.forEach((s) =>
    {
        InitSlidersColor(s);
        UpdateSlidersColor();
    });

    imageOfSound.addEventListener('click', () => {
        if(imageOfSound.src.includes("SoundWhite.png"))
        {
            imageOfSound.src = "../static/assets/SoundMuteWhite.png";
            soundOnMove.volume = 0;
            interactSound.volume = 0;
            sliderSound.volume = 0;
            sfx.value = 0;
            volumeValueOfmusic.value = 0;
            paragraphSfx.textContent = "Mute activé !";
            paragraphMusic.textContent = "Mute activé !";
            DisableSlider(sfx);
            DisableSlider(volumeValueOfmusic);
            SongVolume(mainMusic, volumeValueOfmusic.value);
        }
        else
        {
            imageOfSound.src = "../static/assets/SoundWhite.png";
            soundOnMove.volume = soundVolume;
            interactSound.volume = soundVolume;
            sliderSound.volume = soundVolume;
            sfx.value = soundVolume*100;
            volumeValueOfmusic.value = musicVolume*100;
            EnableSlider(sfx);
            EnableSlider(volumeValueOfmusic);
            SongVolume(mainMusic, musicVolume)
            paragraphSfx.textContent = sfx.value + "%";
            paragraphMusic.textContent = volumeValueOfmusic.value + "%"; 
        }
    });

    luminosity.addEventListener('input', () => {
        PlaySound(sliderSound);
        UpdateBrightness(luminosity);
        paragraphLum.textContent = luminosity.value  + "%";
    });

    sfx.addEventListener('input', () => {
        PlaySound(sliderSound);
        var val = sfx.value / 100;
        soundOnMove.volume = val;
        interactSound.volume = val;
        sliderSound.volume = val;
        soundVolume = val;
        paragraphSfx.textContent = sfx.value + "%";
    });

    volumeValueOfmusic.addEventListener('input', () => 
    {
        PlaySound(sliderSound);
        var val = volumeValueOfmusic.value / 100;
        musicVolume = val;
        SongVolume(mainMusic, val);
        pMusic.textContent = volumeValueOfmusic.value + "%";
    });

    checkPerformanceMode.addEventListener('click', (event) => 
    {
        const testCheck = event.target.checked;
        if(testCheck == true)
        {
            lowPerformanceMode.style.setProperty('display', 'none', 'important');
        }
        else
        {
            lowPerformanceMode.style.setProperty('display', 'block', 'important');
        }
    });

    checkFullScreen.addEventListener('click', (event) => 
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
});

    /* ================================================== */

    /* ================= Functions ==================== */

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
    el.style.setProperty('--range-pct', 0 + '%');
}

function EnableSlider(el)
{
    console.log(el.value);
    el.disabled = false;
    el.style.setProperty('--range-pct', el.value + '%');
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

function InitSlidersColor(event)
{
    const initValue = ((event.value - event.min) / (event.max - event.min)) * 100
    event.style.setProperty('--range-pct', initValue + '%');
}

function UpdateSlidersColor()
{
    const sliders = document.querySelectorAll('.slider');
    sliders.forEach((s) => 
    {
        s.addEventListener('input', function() 
        {
            const ratio = (this.value - this.min) / (this.max - this.min) * 100;
            console.log(ratio);
            this.style.setProperty('--range-pct', ratio + '%');
        });
    })
}



    /* ===================================== */
