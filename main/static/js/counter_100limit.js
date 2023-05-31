var characters_Limits = 100;
$('.edit_about_ta').keyup(function() {
    if ($(this).val().length > characters_Limits) {
         $(this).val($(this).val().substr(0, characters_Limits));

    }
     $('#charCounts').text(this.value.replace(/{.*}/g, '').length);
});
