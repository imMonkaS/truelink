$(".edit_about_ta").hide();
$("#charCounts").hide();
$(".send-btn").hide();
$('.edit_about_hide').click(function(){
  $(".edit_about_ta").toggle();
  $("#charCounts").toggle();
  $(".send-btn").toggle();
});
document.querySelector('.edit_about_ta').value = '';