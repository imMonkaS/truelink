$(document).ready(function(){
    $('.close').click(function(){
        $.ajax({
            type: "POST",
            url: "/messager/?u={{user_with.id}}",
            data: {message_id: $(this).attr('id')},
            headers: {'X-CSRFToken': csrftoken},
            success: function(html){
                console.log($(this))
                $(this).detach()
            }
        })
    });
});