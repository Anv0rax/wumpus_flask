document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("table tr");
    const soundAnimation = document.getElementById("soundTableAnimation");
    const click = document.getElementById('click');
    const table = document.getElementById('table');
    

    click.addEventListener('click', () =>{
        soundAnimation.currentTime = 1;
        soundAnimation.play();
        click.style.display = 'none';
        table.style.display = 'block';

        rows.forEach((row, index) => {
        row.animate(
        [
            { opacity: 0, transform: "translateY(20px)" }, 
            { opacity: 1, transform: "translateY(0)" }
        ], 
        {
            // Each parameter for the rows animations. 
            duration: 500,
            fill: "forwards",
            easing: "ease-out",
            delay: index * 100
        });
    });
    })  
});

function PlaySound(el)
{
    el.currentTime = 0;
    el.play();
}