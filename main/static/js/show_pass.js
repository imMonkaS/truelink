$('.lbl-lan').click(function(){
    if ($(this).parent().prev().attr('type') == 'password'){
        $(this).addClass('view');
        $(this).parent().prev().attr('type', 'text');
    } else {
        $(this).removeClass('view');
        $(this).parent().prev().attr('type', 'password');
    }
    return false;
});