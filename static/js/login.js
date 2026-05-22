document.addEventListener('DOMContentLoaded', function() {
    const inputUserName = document.getElementById("username");
    const inputPswrd = document.getElementById("password");

    let regexUserName = /^[a-zA-Z0-9_]{3,10}$/;
    let regexPswrd = /^.{10,30}$/u;

    inputUserName.addEventListener('keyup', e => { 
        checkValidity(inputUserName, regexUserName);
    });

    inputPswrd.addEventListener('keyup', e => { 
        checkValidity(inputPswrd, regexPswrd);
    });

    const loginForm = document.getElementById('login-form');
    
    loginForm.addEventListener('submit', function(event) {
        if(!checkValidity(inputUserName, regexUserName) 
            || !checkValidity(inputPswrd, regexPswrd))
        {
            event.preventDefault();
        }
    });
});

function checkValidity(input, regex) {
    var tested = regex.test(input.value.trim());
    var redColor = "#FF5A3D";
    var greenColor = "#3DCC6A";

    if(!tested) {
        input.style.color = redColor;
        input.style.borderColor = redColor;
    }
    else {
        input.style.color = greenColor;
        input.style.borderColor = greenColor;
    }
    return tested;
}