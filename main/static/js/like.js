function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function () {
    $(".like").click(function () {
        let liked = 0
        $(this).toggleClass("heart-anim");
        if(this.classList.contains("heart-anim")) {
            $(this).parent().children()[1].innerHTML = $(this).parent().children()[1].innerHTML - (-1)

            liked = true
        }
        else{
            $(this).parent().children()[1].innerHTML = $(this).parent().children()[1].innerHTML - 1

            liked = false
        }

        $.ajax({
            type: "POST",
            url: window.location.href,
            data: {'post_id': $(this).attr('id')},
            headers: {'X-CSRFToken': csrftoken},
            success: function(html){
            }
        });
    });
});
