chat_ta.onkeydown = function(e){
    if (e.keyCode == 13 && !e.shiftKey && chat_ta.value.replace(/ /g,'').length != 0){
        e.preventDefault()
        var form = $("#send_message_form").serialize();
        $.ajax({
            type: "POST",
            url: window.location.href,
            data: form,
            success: function(html){
                chat_ta.value='';
            }
        });
    }
    if (e.keyCode == 13 && chat_ta.value.replace(/ /g,'').length == 0){
        e.preventDefault()
    }
}