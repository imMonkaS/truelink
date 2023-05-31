// When the user clicks on div, open the popup
'use strict';

function outsideClick(event, notelem)	{
    notelem = $(notelem); // jquerize (optional)
    // check outside click for multiple elements
    var clickedOut = true, i, len = notelem.length;
    for (i = 0;i < len;i++)  {
        if (event.target == notelem[i] || notelem[i].contains(event.target)) {
            clickedOut = false;
        }
    }
    if (clickedOut) return true;
    else return false;
}

popupFunc()

function popupFunc() {
    let popupDiv = document.querySelector(".userIcon");
    let popup = document.querySelector('.popuptext');
    
    popupDiv.onclick = function(){
        popup.classList.add('show')
    }
    window.onclick = function(e){
        if (outsideClick(e, popupDiv)){
            popup.classList.remove("show");
        }
    }
}
