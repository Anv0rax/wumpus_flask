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

let movementTop = 'space'
let movementBot = 'space'
let movementLeft = 'space'
let movementRight = 'space'

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
        listBtnMoveIg[2].click();
    }
    else if(event.key === 'ArrowRight' || event.key === movementRight)
    {
        event.preventDefault();
        listBtnMoveIg[3].click();
    }
}

// function addListenerBtnMoveIg() {
//     for (let i = 0; i < 4; i++) {
//         listBtnMoveIg[i].onclick = () => {
//             gameMove(i);
//         };
//         listBtnMoveIg[i].type = "button";
//     }
// }

function gameMove(n) {
    switch (n) {
        case 0 :
            xMoveIg.value = 0;
            yMoveIg.value = -1;
            formMoveIg.submit();
            break;
        case 1 :
            xMoveIg.value = 0;
            yMoveIg.value = 1;
            formMoveIg.submit();
            break;
        case 2 : 
            xMoveIg.value = -1;
            yMoveIg.value = 0;
            formMoveIg.submit();
            break;
        case 3 : 
            xMoveIg.value = 1;
            yMoveIg.value = 0;
            formMoveIg.submit();
            break;
    }
}