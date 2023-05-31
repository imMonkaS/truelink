const passwordEl = document.querySelector("#pwd");
const eyeButton = document.querySelector(".fa");
const eyeSpan = document.querySelector("#eye");
const eyeS = document.querySelector(".s");
const eyeSpanSecond = document.querySelector("#eyeSec");
const passSec = document.querySelector("#pwdSec");
let isPass = true;
let isPasss = true;

eyeSpan.addEventListener("click", togglePass, false);
eyeSpanSecond.addEventListener("click", togglePasss, false);

function show() {
    passwordEl.setAttribute('type', 'text');
    eyeButton.classList.remove("fa-eye");
    eyeButton.classList.add("fa-eye-slash");
}

function hide() {
    passwordEl.setAttribute('type', 'password');
    eyeButton.classList.remove("fa-eye-slash");
    eyeButton.classList.add("fa-eye");
}

function shows() {
    passSec.setAttribute('type', 'text');
    eyeS.classList.remove("fa-eye");
    eyeS.classList.add("fa-eye-slash");
}

function hides() {
    passSec.setAttribute('type', 'password');
    eyeS.classList.remove("fa-eye-slash");
    eyeS.classList.add("fa-eye");
}

function togglePass() {
    if (isPass) {

        show();
        isPass = false;

    } else {

        hide();
        isPass = true;

    }
}

function togglePasss() {
    if (isPasss) {

        shows();
        isPasss = false;

    } else {

        hides();
        isPasss = true;

    }
}
