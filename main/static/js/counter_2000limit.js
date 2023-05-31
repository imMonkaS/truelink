$('.post-message-ta').value = '';

var characters_Limit = 2000;
$('.post-message-ta').keyup(function() {
    if ($(this).val().length > characters_Limit) {
         $(this).val($(this).val().substr(0, characters_Limit));

    }
     $('#charCount').text(this.value.replace(/{.*}/g, '').length);
});