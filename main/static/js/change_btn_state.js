function change_button_state(btn, activity){
    if (activity == false){
        btn.disabled = true;
        btn.style.cursor = 'default';
        btn.children[0].style.opacity = '0';
    }
    else {
        btn.disabled = false;
        btn.style.cursor = 'pointer';
        btn.children[0].style.opacity = '1';
    }
}

change_button_state(chat_send_btn, false);