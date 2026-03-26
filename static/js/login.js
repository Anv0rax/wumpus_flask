document.addEventListener('DOMContentLoaded', function()
{
    // TODO : savoir enlever le currentColor et currentTool
    let currentColor = "none";
    let currentTool = "pencil";

    function initTools()
    {
        let pencil = document.getElementById('pencil');
        let eraser = document.getElementById('eraser');
        let bucket = document.getElementById('bucket');

        pencil.style.filter = 'drop-shadow(0 0 5px #00d4ff)';

        if(pencil)
        {
            pencil.addEventListener('click', function(e)
            {
                e.preventDefault();
                currentTool = "pencil";
                eraser.style.filter = 'none';
                bucket.style.filter = "none";
                pencil.style.filter = 'drop-shadow(0 0 5px #00d4ff)';
                console.log("Le crayon a été sélectionné - mode de tools en " + currentTool);
            });
        }

        if(eraser)
        {
            eraser.addEventListener('click', function(e)
            {
                e.preventDefault();
                currentTool = "eraser";
                eraser.style.filter = 'drop-shadow(0 0 5px #00d4ff)';
                pencil.style.filter = 'none';
                bucket.style.filter = "none";
                console.log("La gomme est selectionne - mode de tools en " + currentTool);
            });
        }

        if(bucket)
        {
            bucket.addEventListener('click', function(e)
            {
                e.preventDefault();
                currentTool = "bucket";
                bucket.style.filter = "drop-shadow(0 0 5px #00d4ff)";
                eraser.style.filter = "none";
                pencil.style.filter = "none";
                console.log("Le Seau a été sélectionné - mode de tools en " + currentTool);
            });
        }
        // pencil = null;
        // eraser = null;
        // bucket = null;
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

        if (colors.length > 0) // Remeber that I have a list with the querySelectorAll. Thats means the list can't have a null value! I have to check the length of the list.
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
        let gridElement = document.querySelector('.grid');

        if(gridElement)
        {
            for(let i = 0; i < 24 * 24; i++)
            {
                let cell = document.createElement("div");
                cell.classList.add("cell");

                gridElement.appendChild(cell);

                cell = null;
            }

            let cells = document.querySelectorAll('.cell');
            cells.forEach(cell => 
            {
                cell.addEventListener('click', activate);
                cell.style.backgroundColor = "transparent";
            });

            cells = null
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
        //let cellSize = 1;
        /* For now, the grid is 24x24. One cell equals to one square on the grid, so the cellSize is 1.*/
        let canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size; // So my image, will the the exact size of the grid.
        let ctx = canvas.getContext('2d'); // im forced to use this, otherwise the fillRect and other methods CANNOT be used, so important to draw anything.

        /* im going to get every cell of the grid to transform them in the png format. cells, is going to be a list of numbers for each grid. Each number is of course unique.*/
        let cells = document.querySelectorAll('.grid .cell');

        cells.forEach((cell, index) =>
        { // "index" is the position of the cell in the grid (3rd row, 2nd column for example.). "cell" is my html element, which im going to extract the colors of each cell to put them on the canvas. (For example, the cell on 1;1 is going to be white, im extracting then the color white to copy it to the canvas.)
            let x = index % size;
            let y = Math.floor(index / size);
            // First, im going to calculate the modulo of the index (which is for reminder the position of the index in the grid, be careful that the first cell of all the grid is 0, and not one.)
            // For example, lets say that I have a cell with an index of 67.
            // 67 % 24 = 19 (its the rest of my division) so my cell is in the position 19 in the x axis.

            // Then, I divide my index my the size to get my y axis. Im going to floor the answer to not get incorrect values, since one grid = a unique index
            // 67 / 24 = 2,79166666.... Im flooring the value and I get 2 ! (be careful that floor round off to the nearest whole number)
            // My cell is located is x = 19 and y = 2.

            let color = window.getComputedStyle(cell).backgroundColor;

            ctx.fillStyle = color;
            ctx.fillRect(x,y,1,1);
        })

        /* now its the part where I convert the canvas into png image ! */
        let dataURL = canvas.toDataURL('image/png');

        /* with this done, i can now show the preview of the image directly in the page. */
        let previewImg = document.getElementById("user-pixel-art");
        previewImg.src = dataURL;
        previewImg.style.display = 'block';

        /* Everything is done, so now I will close the grid window. */
        document.querySelector('.container-pixArtMaker').classList.remove('active');

        size = null;
        cellSize = null;
        canvas = null;
        ctx = null;
        cells = null;
        dataURL = null;
        previewImg = null;
    }

    /* TO HIDE AND SHOW THE GRID */

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

    /* COLOR AND CREATION OF THE GRID */

    function activate(event)
    {
        if(currentTool === 'eraser')/*event.target.style.backgroundColor && event.target.style.backgroundColor !== 'transparent'*/
        {
            event.target.style.backgroundColor = 'transparent';
        }
        else if(currentTool === 'pencil')
        {
            event.target.style.backgroundColor = currentColor;
        }
        else if(currentTool ==='bucket')
        {
            let cells = document.querySelectorAll('.cell');
            cells.forEach(cell => 
            {
                cell.addEventListener('click', activate);
                cell.style.backgroundColor = currentColor;
            });
            cells = null
        }
    }

    function ChangeColor(event)
    {
        let allTheOtherColors = document.querySelectorAll('.color');
        let cells = document.querySelectorAll('.cell');

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