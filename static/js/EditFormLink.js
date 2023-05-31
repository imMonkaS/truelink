let limitL = 1;
let currentAmountL = 0;

spanEditorLink.onclick = function () {

    if (currentAmountL < limitL) {
        let linkUser = document.getElementById("menuDBCLAdres").innerHTML;
        let elemLink = document.getElementById('linkForm');
        let oldDivEditLink = document.createElement("div");
        oldDivEditLink.className = "settTextDiv";
        elemLink.appendChild(oldDivEditLink);

        let oldSpanEditLink = document.createElement("span");
        oldSpanEditLink.className = "grayHTTPS spanLink text-default";
        oldSpanEditLink.innerHTML = "https://truelink.com/";
        oldDivEditLink.appendChild(oldSpanEditLink);

        let inputEditLink = document.createElement("input");
        inputEditLink.className = "editValue settingEditorInput inputLink text-default";
        inputEditLink.value = linkUser;
        inputEditLink.maxlength = "32";
        oldDivEditLink.appendChild(inputEditLink);

        let buttonCofirmEditLink = document.createElement("button");
        buttonCofirmEditLink.className = "buttonConfEdit text-default";
        buttonCofirmEditLink.innerHTML = "Изменить ссылку";
        oldDivEditLink.appendChild(buttonCofirmEditLink);


        currentAmountL++;

        buttonCofirmEditLink.onclick = function () {
            if (inputEditLink.value != "") {
                let userNewLink = inputEditLink.value;
                oldDivEditLink.remove();

                let changeLink = document.getElementById("menuDBCLAdres");
                changeLink.innerHTML = userNewLink;
                let previewLink = document.getElementById("prevLink");
                previewLink.innerHTML = userNewLink;
                currentAmountL = 0;

            }
        }
    }

}
