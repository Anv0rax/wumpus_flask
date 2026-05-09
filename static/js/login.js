document.addEventListener('DOMContentLoaded', function()
{
    let currentColor = "none";
    let currentTool = "pencil";
    let greenColor = "#3DCC6A";
    let redColor = "#FF5A3D";

    const inputUserName = document.getElementById("username");
    const inputPswrd = document.getElementById("password");
    const confirmPswrd = document.getElementById("confirmPassword");
    const helpUserName = document.getElementById("helpUserName");
    const helpPassword = document.getElementById("helpPswrd");

    const liHelpUsername = document.querySelectorAll(".helpUserNameItem");
    const liHelpPswd = document.querySelectorAll(".helpPswrdItem");

    let regexUserName = /^[a-zA-Z0-9_]{3,10}$/
    let listRegexPswrd = [/^.{3,10}$/, /[A-Z]/, /[a-z]/, /[0-9]/];

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
            }

            let cells = document.querySelectorAll('.cell');
            cells.forEach(cell =>
            {
                cell.addEventListener('click', activate);
                cell.style.backgroundColor = "transparent";
            });
        }
    }

    function initToggleGrid()
    {
        let toggleGrid = document.getElementById('showGrid');
        if(toggleGrid)
        {
            toggleGrid.addEventListener('click', ShowTheGrid);
        }
    }

    function initLeaveTheGrid()
    {
        let leaveTheGrid = document.getElementById('leave');
        if(leaveTheGrid)
        {
            leaveTheGrid.addEventListener('click', HideTheGrid);
        }
    }

    function initRegisterButton()
    {
        let registerBtn = document.getElementById('register');
        if(registerBtn)
        {
            registerBtn.addEventListener('click', function()
            {
                window.location.href = '/register';
            });
        }
    }

    function initReturnButton()
    {
        let returnBtn = document.getElementById('returnLogin');
        if(returnBtn)
        {
            returnBtn.addEventListener('click', function()
            {
                window.location.href = '/login';
            });
        }
    }

    initSaveGrid();
    initColors();
    initGridElement();
    initToggleGrid();
    initLeaveTheGrid();
    initRegisterButton();
    initReturnButton();
    initTools();

    function Save_Pixart()
    {
        let size = 24;
        let canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        let ctx = canvas.getContext('2d');

        let cells = document.querySelectorAll('.grid .cell');
        cells.forEach((cell, index) =>
        {
            let x = index % size;
            let y = Math.floor(index / size);
            let color = window.getComputedStyle(cell).backgroundColor;
            ctx.fillStyle = color;
            ctx.fillRect(x, y, 1, 1);
        });

        let dataURL = canvas.toDataURL('image/png');
        let previewImg = document.getElementById("user-pixel-art");
        previewImg.src = dataURL;
        previewImg.style.display = 'block';

        let imgStringBase64 = dataURL.replace(/^data:image\/png;base64,/, "");
        let hiddenInput = document.getElementById("icon-data");
        if(hiddenInput)
        {
            hiddenInput.value = imgStringBase64;
        }

        document.querySelector('.container-pixArtMaker').classList.remove('active');
    }

    function HideTheGrid(e)
    {
        e.preventDefault();
        let maker = document.querySelector('.container-pixArtMaker');
        if(maker)
        {
            maker.classList.remove('active');
        }
    }

    function ShowTheGrid(e)
    {
        e.preventDefault();
        let maker = document.querySelector('.container-pixArtMaker');
        if(maker)
        {
            maker.classList.add('active');
        }
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
            let cells = document.querySelectorAll('.cell');
            cells.forEach(cell =>
            {
                cell.style.backgroundColor = currentColor;
            });
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
    }

    function checkValidUserName()
    {
        if(!inputUserName || !helpUserName) return true;
        let testInput = inputUserName.value.trim();

        if(regexUserName.test(testInput))
        {
            helpUserName.style.color = greenColor;
            inputUserName.style.color = greenColor;
            inputUserName.style.borderColor = greenColor;
            return true;
        }
        else
        {
            helpUserName.style.color = redColor;
            inputUserName.style.color = redColor;
            inputUserName.style.borderColor = redColor;
            return false;
        }
    }

    function checkValidPassword()
    {
        if(!inputPswrd || liHelpPswd.length === 0) return true;
        let nbrErrors = 0;
        let testInput = inputPswrd.value.trim();

        for(let i = 0; i < listRegexPswrd.length; i++)
        {
            if (listRegexPswrd[i].test(testInput)) {
                liHelpPswd[i].style.color = greenColor;
            } else {
                nbrErrors += 1;
                liHelpPswd[i].style.color = redColor;
            }
        }

        if(nbrErrors === 0)
        {
            inputPswrd.style.color = greenColor;
            inputPswrd.style.borderColor = greenColor;
            return true;
        }
        else
        {
            inputPswrd.style.color = redColor;
            inputPswrd.style.borderColor = redColor;
            return false;
        }
    }

    if(inputUserName)
    {
        inputUserName.addEventListener('keyup', checkValidUserName);
    }

    if(inputPswrd)
    {
        inputPswrd.addEventListener('keyup', checkValidPassword);
    }

    const loginForm = document.getElementById('login-form');
    if(loginForm)
    {
        loginForm.addEventListener('submit', function(event)
        {
            let isPswrdValid = checkValidPassword();
            let isUsernameValid = checkValidUserName();
            let isPswrdConfirmValid = true;

            if(confirmPswrd && inputPswrd)
            {
                isPswrdConfirmValid = (confirmPswrd.value === inputPswrd.value && inputPswrd.value !== "");
                if(!isPswrdConfirmValid)
                {
                    alert("The passwords in confirm password and password are not matching.");
                }

                if(!isUsernameValid || !isPswrdValid || !isPswrdConfirmValid)
                {
                    event.preventDefault();
                }
            }
        });
    }
});
