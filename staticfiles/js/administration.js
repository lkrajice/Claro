$(document).ready(function(){
    $("span[name=studentid]").on('click', function(){
        var a = $("span[name=studentid]").attr('value');
        alert("AA")
        $("#btn_modify_student").attr('value', a);
    })
});
