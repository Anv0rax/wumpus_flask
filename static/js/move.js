window.addEventListener('load', () => { 

    formMoveIg = document.getElementById("moving_ig");
    xMoveIg = document.getElementById("form_move-x");
    yMoveIg = document.getElementById("form_move-y");

    // movementTop = event.key
    // movementBot = event.key
    // movementLeft = event.key
    // movementRight = event.key

    let movementTop = 'space'
    let movementBot = 'space'
    let movementLeft = 'space'
    let movementRight = 'space'

    // formMoveIg.onsubmit = () => {
    //     verifyFormMoveIg();
    // }

    document.onkeydown = (event) => {
		pressKey(event);
	};

    listBtnMoveIg = document.querySelectorAll(".btn_move_ig");

    function pressKey(event)
    {
        if(event.key === 'ArrowUp' || event.key === movementTop)
        {
            event.preventDefault();
            gameMove(0);
        }
        else if(event.key === 'ArrowDown' || event.key === movementBot)
        {
            event.preventDefault();
            gameMove(1);
        }
        else if(event.key === 'ArrowLeft' || event.key === movementLeft)
        {
            event.preventDefault();
            gameMove(2);
        }
        else if(event.key === 'ArrowRight' || event.key === movementRight)
        {
            event.preventDefault();
            gameMove(3);
        }
    }

    function addListenerBtnMoveIg() {
        for (let i = 0; i < 4; i++) {
            listBtnMoveIg[i].onclick = () => {
                gameMove(i);
            };
        }
    }

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

    function verifyFormMoveIg() {

    }

    addListenerBtnMoveIg();

});