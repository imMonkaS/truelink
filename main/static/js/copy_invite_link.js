document.getElementById('copier').addEventListener('click', function(e) {
    var copytext = document.createElement('input');
    copytext.value = "https://truelink.pythonanywhere.com/servers/{{server.id}}/invite/";
    document.body.appendChild(copytext);
    copytext.select();
    document.execCommand('copy');
});