let passwordAccountUserP = "123"; // Значение берем из ДБ
let limitP = 1;
let currentAmountP = 0;


spanEditorPassword.onclick = function () {
    if (currentAmountP < limitP) {
        let elem = document.getElementById('passForm');
        let divAllInput = document.createElement("div");
        divAllInput.className = "settTextDiv";
        elem.appendChild(divAllInput);

        let formAllInput = document.createElement("form");
        divAllInput.appendChild(formAllInput);

        let inputEditPass1 = document.createElement("input");
        inputEditPass1.className = "editValue settingEditorInput text-default";
        inputEditPass1.placeholder = "Введите ваш пароль";
        inputEditPass1.type = "password";
        inputEditPass1.setAttribute("required", "");
        formAllInput.appendChild(inputEditPass1);

        let firstBr1 = document.createElement("br");

        let inputEditPass2 = document.createElement("input");
        inputEditPass2.className = "editValue settingEditorInput text-default";
        inputEditPass2.placeholder = "Введите новый пароль";
        inputEditPass2.type = "password";
        inputEditPass2.setAttribute("required", "");

        let firstBr2 = document.createElement("br");

        let inputEditPass3 = document.createElement("input");
        inputEditPass3.className = "editValue settingEditorInput text-default";
        inputEditPass3.placeholder = "Введите новый пароль";
        inputEditPass3.type = "password";
        inputEditPass3.setAttribute("required", "");

        let buttonCofirmEditPass = document.createElement("button");
        buttonCofirmEditPass.className = "buttonConfEdit text-default";
        buttonCofirmEditPass.innerHTML = "Изменить пароль";

        formAllInput.appendChild(inputEditPass1);
        formAllInput.appendChild(firstBr1);
        formAllInput.appendChild(inputEditPass2);
        formAllInput.appendChild(firstBr2);
        formAllInput.appendChild(inputEditPass3);
        formAllInput.appendChild(buttonCofirmEditPass);
        currentAmountP++;

        buttonCofirmEditPass.onclick = function () {
            if (inputEditPass1.value == "" || inputEditPass2.value == "" || inputEditPass3.value == "") {
                return;
            } else {
                if (inputEditPass1.value == passwordAccountUserP) {
                    if (inputEditPass2.value == inputEditPass3.value) {
                        divAllInput.remove();

                        let editpass = document.getElementById("menuDBCLPassword");
                        editpass.innerHTML = "Был изменен только что";

                        currentAmountP = 0;
                    } else {
                        inputEditPass2.placeholder = "Пароли различаются";
                        inputEditPass3.placeholder = "Пароли различаются";
                        inputEditPass1.value = "";
                        inputEditPass2.value = "";
                        inputEditPass3.value = "";
                    }
                } else {
                    inputEditPass1.placeholder = "Пароль неправильный";
                    inputEditPass1.value = "";
                    inputEditPass2.value = "";
                    inputEditPass3.value = "";
                }
            }
        }
    }

}
