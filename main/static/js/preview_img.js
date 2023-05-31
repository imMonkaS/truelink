var loadFile = function(event) {
    var reader = new FileReader();
    reader.onload = function(){
    var output = document.getElementById('output');
    output.src = reader.result;
};

reader.readAsDataURL(event.target.files[0]);
};

$("#imag").change(function() {
  $('.btn-rmv1').addClass('rmv');
});

$("#removeImage1").click(function(e) {
  e.preventDefault();
  $("#imag").val("");
  $("#output").attr("src", "");
  $('.btn-rmv1').removeClass('rmv');
});
