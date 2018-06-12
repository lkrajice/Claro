function resize()
{
    console.log('help');
    let divs = document.getElementsByClassName("class-link-wrapper");
    for (let i = 0; i < divs.length; i++) {
        let div = divs[i];
        let div_parent = div.parentNode;

        div.style.width = (div_parent.offsetWidth - 120) + 'px';
    }
}

function make_loop() {
    let refresh = setInterval(resize, 10);
    setTimeout(function() {
        clearInterval(refresh);
    }, 1000);
}

$(document).ready(function() {
    $(document).on('expanded.pushMenu', make_loop);
    $(document).on('collapsed.pushMenu', make_loop);

    setInterval(resize, 250);
});
resize();
