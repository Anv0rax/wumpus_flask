document.addEventListener('DOMContentLoaded', () => {
    let currentColor = "none";
    let currentTool = "pencil";



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

        document.getElementById("profile-form").submit();

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