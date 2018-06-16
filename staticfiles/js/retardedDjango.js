function replaceDiacritics(input){
    var diacritics = [["ě","e"], ["š","s"], ["č","c"], ["ř","r"], ["ž", "z"], ["ý","y"], ["á","a"], ["í","i"], ["é","e"], ["ň", "n"]]
    var word = ""
    var splitted_word = input.split("")
    for(var i = 0; i<splitted_word.length;i++){
        for(var y = 0; y < diacritics.length; y++) {
            if (splitted_word[i] == diacritics[y][0]) {
                splitted_word[i] = diacritics[y][1]
            }
        }
    }
    for(var i = 0; i < splitted_word.length; i++) {
        word +=splitted_word[i]
    }
  return word;
};

$(document).ready(function(){
    $("#student_name").keyup(function(){
        var data = replaceDiacritics($("#student_name").val().toLowerCase());
        console.log("data" + data)
        var handle_space = data.replace(" ", ".");
        $("#student_mail").val(handle_space+"@sspbrno.cz");

    });
})
