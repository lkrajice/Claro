function resize()
{
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

function trigger_vote_modal(element) {
    header = $(element).find("div.card-body > h4.card-title")
    student_name = header.text()
    student_id = header.attr("data-id")

    modal = $("#myModal");
    modal.find("span.modal-student-name").each(function() {
        $(this).text(student_name)
    })
    modal.find("#modal_student_id").val(student_id)
    modal.modal();
}

$(document).ready(function() {
    $(document).on('expanded.pushMenu', make_loop);
    $(document).on('collapsed.pushMenu', make_loop);

    setInterval(resize, 250);
});
resize();
