document.addEventListener('DOMContentLoaded', () =>
{
    /* ======== Constantes ========*/

    const checkDifficulty = document.getElementById('difficulty-choice');
    const form = document.getElementById('form');
    const checkBouton = document.querySelectorAll('.selectGamemode');
    

    /* ====================================== */

    checkDifficulty.addEventListener('change', (el) => {
        const val = checkDifficulty.value;
        if(val == 0) checkDifficulty.style.color = "#3DCC6A";
        if(val == 1) checkDifficulty.style.color = "#FFBE4D";
        if(val == 2) checkDifficulty.style.color = "#FF5A3D";
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        if ((checkDifficulty.value == 0 || checkDifficulty.value == 1 || checkDifficulty.value == 2)
            && (form.express.value == 0 || form.express.value == 1)
            && (form.blind.value == 0 || form.blind.value == 1)) {
            form.submit();
        }
    });
});