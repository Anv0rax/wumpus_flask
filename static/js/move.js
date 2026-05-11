window.addEventListener('load', () => {

    formMoveIg = document.getElementById("ig_moving");
    xMoveIg = document.getElementById("ig_form_move-x");
    yMoveIg = document.getElementById("ig_form_move-y");

    // let movementTop = event.key
    // let movementBot = event.key
    // let movementLeft = event.key
    // let movementRight = event.key

    document.onkeydown = (event) => {
		pressKey(event);
	};

    listBtnMoveIg = document.querySelectorAll(".ig_btn_move");

    // addListenerBtnMoveIg();

});

let movementTop = 'jsp'
let movementBot = 'jsp'
let movementLeft = 'jsp'
let movementRight = 'jsp'
let switchShoot = 'jsp'

function pressKey(event)
{
    if(event.key === 'ArrowUp' || event.key === movementTop)
    {
        event.preventDefault();
        listBtnMoveIg[0].click();
    }
    else if(event.key === 'ArrowDown' || event.key === movementBot)
    {
        event.preventDefault();
        listBtnMoveIg[1].click();
    }
    else if(event.key === 'ArrowLeft' || event.key === movementLeft)
    {
        event.preventDefault();
        listBtnMoveIg[3].click();
    }
    else if(event.key === 'ArrowRight' || event.key === movementRight)
    {
        event.preventDefault();
        listBtnMoveIg[4].click();
    }
    else if(event.key === 'CapsLock' || event.key === movementRight)
    {
        event.preventDefault();
        listBtnMoveIg[2].click();
    }
}

