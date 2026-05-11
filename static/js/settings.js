// TODO : Essayer de faire le lien entre la page du choix de la difficulté, et que la aussi le son par exemple de la musique soit la même dans le menu paramétres ou dans le menu choix difficulté.

document.addEventListener('DOMContentLoaded', () => {

    /* ========= the const ==========*/
    /*const soundOnMove = document.getElementById('son1');
    const interactSound = document.getElementById('son2');
    const lowPerformanceMode = document.getElementById('backgroundAnimationRings');
    const checkBouton = document.querySelectorAll('.check');
    const sliderSound = document.getElementById('son4');

    const luminosity = document.getElementById('light');
    const sfx = document.getElementById('sfx');
    const imageOfSound = document.getElementById('sound');
    const paragraphLum = document.getElementById('pLum');
    const paragraphSfx = document.getElementById('pSfx');


    const checkPerformanceMode = document.getElementById('checkPerf');

    const sliders = document.querySelectorAll('.slider');*/

    /* =========================================== */
    let currentColor = "none";
    let currentTool = "pencil";
    /* ======== the code ========== */

    /*let soundVolume = 0.25;
    sliderSound.volume = soundVolume;


    paragraphLum.textContent = luminosity.value + '%';
    paragraphSfx.textContent = sfx.value + "%";

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
            paragraphSfx.textContent = "Mute activé !";
            DisableSlider(sfx);
        }
        else
        {
            imageOfSound.src = "../static/assets/SoundWhite.png";
            soundOnMove.volume = soundVolume;
            interactSound.volume = soundVolume;
            sliderSound.volume = soundVolume;
            sfx.value = soundVolume*100;
            EnableSlider(sfx);
            paragraphSfx.textContent = sfx.value + "%";
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
    });*/



    function initTools()
    {
        let pencil = document.getElementById('pencil');
        let eraser = document.getElementById('eraser');
        let bucket = document.getElementById('bucket');

        if(!pencil || !eraser || !bucket) return;

        pencil.style.filter = 'drop-shadow(0 0 5px #00d4ff)';

        pencil.addEventListener('click', function(e)
        {
            e.preventDefault();
            currentTool = "pencil";
            eraser.style.filter = 'none';
            bucket.style.filter = "none";
            pencil.style.filter = 'drop-shadow(0 0 5px #00d4ff)';
        });

        eraser.addEventListener('click', function(e)
        {
            e.preventDefault();
            currentTool = "eraser";
            eraser.style.filter = 'drop-shadow(0 0 5px #00d4ff)';
            pencil.style.filter = 'none';
            bucket.style.filter = "none";
        });

        bucket.addEventListener('click', function(e)
        {
            e.preventDefault();
            currentTool = "bucket";
            bucket.style.filter = "drop-shadow(0 0 5px #00d4ff)";
            eraser.style.filter = "none";
            pencil.style.filter = "none";
        });
    }

    function initSaveGrid()
    {
        let saveGrid = document.getElementById('confirm');

        if(saveGrid)
        {
            saveGrid.addEventListener('click', Save_Pixart);
        }

        saveGrid = null;
    }

    function initColors()
    {
        let colors = document.querySelectorAll('.color');

        if (colors.length > 0)
        {
            colors.forEach(color =>
            {
                color.addEventListener('click', ChangeColor);
            });
        }
        colors = null;
    }

    function initGridElement()
    {
        let gridElement = document.querySelector('.pixart-grid');

        if(gridElement)
        {
            for(let i = 0; i < 24 * 24; i++)
            {
                let cell = document.createElement("div");
                cell.classList.add("cell");

                gridElement.appendChild(cell);

                cell = null;
            }

            let cells = document.querySelectorAll('.pixart-grid .cell');
            cells.forEach(cell =>
            {
                cell.addEventListener('click', activate);
                cell.style.backgroundColor = "transparent";
            });

            cells = null;
        }

        gridElement = null;
    }

    function initToggleGrid()
    {
        let toggleGrid = document.getElementById('showGrid');

        if(toggleGrid)
        {
            toggleGrid.addEventListener('click', ShowTheGrid);
        }

        toggleGrid = null;
    }

    function initLeaveTheGrid()
    {
        let leaveTheGrid = document.getElementById('leave');

        if(leaveTheGrid)
        {
            leaveTheGrid.addEventListener('click', HideTheGrid);
        }

        leaveTheGrid = null;
    }

    initSaveGrid();
    initColors();
    initGridElement();
    initToggleGrid();
    initLeaveTheGrid();
    initTools();
    //DisableGridGame();

    function Save_Pixart()
    {
        let size = 24;
        let canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        let ctx = canvas.getContext('2d');

        let cells = document.querySelectorAll('.pixart-grid .cell');

        cells.forEach((cell, index) =>
        {
            let x = index % size;
            let y = Math.floor(index / size);
            let color = window.getComputedStyle(cell).backgroundColor;

            ctx.fillStyle = color;
            ctx.fillRect(x,y,1,1);
        });

        let dataURL = canvas.toDataURL('image/png');

        let previewImg = document.getElementById("user-pixel-art");
        if (previewImg) {
            previewImg.src = dataURL;
            previewImg.style.display = 'block';
        }

        let imgStringBase64 = dataURL.replace(/^data:image\/png;base64,/, "");

        let hiddenInput = document.getElementById("icon-data");
        if(hiddenInput)
            hiddenInput.value = imgStringBase64;

        document.getElementById("settings-form").submit();

        document.querySelector('.container-pixArtMaker').classList.remove('active');

        size = null;
        canvas = null;
        ctx = null;
        cells = null;
        dataURL = null;
        previewImg = null;
        imgStringBase64 = null;
        hiddenInput = null;
    }

    function HideTheGrid(e)
    {
        e.preventDefault();
        let maker = document.querySelector('.container-pixArtMaker');

        maker.classList.remove('active');
        maker = null;
    }

    function ShowTheGrid(e)
    {
        e.preventDefault();
        let maker = document.querySelector('.container-pixArtMaker');

        maker.classList.add('active');

        maker = null;
    }

    function activate(event)
    {
        if(currentTool === 'eraser')
        {
            event.target.style.backgroundColor = 'transparent';
        }
        else if(currentTool === 'pencil')
        {
            event.target.style.backgroundColor = currentColor;
        }
        else if(currentTool === 'bucket')
        {
            let cells = document.querySelectorAll('.pixart-grid .cell');
            cells.forEach(cell =>
            {
                cell.style.backgroundColor = currentColor;
            });
            cells = null;
        }
    }

    function ChangeColor(event)
    {
        let allTheOtherColors = document.querySelectorAll('.color');
        let cells = document.querySelectorAll('.pixart-grid .cell');

        allTheOtherColors.forEach(notSelectedColor => {
            notSelectedColor.style.border = "none";
        });
        currentColor = event.target.attributes["data-color"].value;

        cells.forEach(cell =>
        {
            cell.addEventListener('mouseover', function()
            {
                cell.style.boxShadow = "inset 0 0 0 1.5px black";
                cell.style.animation = "borderPulsing 2s infinite ease-in-out";
            });
            cell.addEventListener('mouseout', function()
            {
                cell.style.animation = "none";
                cell.style.boxShadow = "none";
            });
        });

        event.target.style.border = "2px solid orange";

        allTheOtherColors = null;
    }
});

    /* ================================================== */

    /* ================= Functions ==================== */

/*function PlaySound(el)
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
    el.disabled = false;
    el.style.setProperty('--range-pct', el.value + '%');
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
            this.style.setProperty('--range-pct', ratio + '%');
        });
    })
}

function DisableGridGame()
{
    const checkTheGrid = document.getElementById('checkGrid');

    if(checkTheGrid) {
        if (localStorage.getItem('checkgriddisable') === "true") {
            checkTheGrid.checked = true;
        }

        // On utilise 'el' ou 'checkTheGrid' au lieu de 'this'
        checkTheGrid.addEventListener('input', () => {
            localStorage.setItem('checkgriddisable', checkTheGrid.checked);
            console.log("Status grille enregistré :", checkTheGrid.checked);
        });
    }
} */



    /* ===================================== */
