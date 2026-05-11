document.addEventListener('DOMContentLoaded', function()
{
    const inputUserName = document.getElementById("username");
    const inputPswrd = document.getElementById("password");
    
    let regexUserName = /^[a-zA-Z0-9_]{3,10}$/
    let regexPswrd = /^.{10,30}$/u;
    
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function(event)
    {
        let testUsrname = inputUserName.value.trim();
        let testMdp = inputPswrd.value.trim();

        if(!regexUserName.test(testUsrname) || !regexPswrd.test(testMdp))
        {
            event.preventDefault();
        }
    });
});