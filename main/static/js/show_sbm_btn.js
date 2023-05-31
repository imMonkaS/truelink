chat_ta.onfocus = function(){
    setInterval(function(){
        if(chat_ta.value.replace(/ /g,'').length != 0){
            change_button_state(chat_send_btn, true);
        }
        else{
            change_button_state(chat_send_btn, false);
        }
    }, 100);
}