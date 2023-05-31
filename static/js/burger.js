window.onload = function () {
    document.querySelector(".c-hamburger").addEventListener("click", function (e) {
        e.preventDefault();
        if (this.classList.contains('is-active')) {
            this.classList.remove("is-active");
            document.querySelector('#menu').classList.remove('nav-active');
            document.body.classList.remove('body-active');
            document.getElementById('chmo').style.left = "165px";
            document.getElementById('chort').style.marginLeft = "0px";
        }
        else {
            this.classList.add("is-active");
            document.querySelector('#menu').classList.add('nav-active');
            document.body.classList.add('body-active');
            document.getElementById('chmo').style.left = "-120px";  
            document.getElementById('chort').style.marginLeft = "-175px";
        }
    });
}


