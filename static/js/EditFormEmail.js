let passwordAccountUser = "123"; // Значение берем из ДБ
let limit = 1;
let currentAmount = 0;

spanEditorEmail.onclick = function () {
    if (currentAmount < limit) {
        let elem = document.getElementById('emailForm');
        let divAllInputEmail = document.createElement("div");
        divAllInputEmail.className = "settTextDiv";
        elem.appendChild(divAllInputEmail);

        let formAllInputEmail = document.createElement("form");

        let inputEditEmail1 = document.createElement("input");
        inputEditEmail1.className = "editValue settingEditorInput text-default";
        inputEditEmail1.placeholder = "Введите пароль";
        inputEditEmail1.type = "password";
        inputEditEmail1.setAttribute("required", "");

        let firstBrEmail = document.createElement("br");

        let inputEditEmail2 = document.createElement("input");
        inputEditEmail2.className = "editValue settingEditorInput text-default";
        inputEditEmail2.placeholder = "Введите новую почту";
        inputEditEmail2.type = "email";
        inputEditEmail2.setAttribute("required", "");

        let secondBrEmail = document.createElement("br");

        let buttonConfEditEmail = document.createElement("button");
        buttonConfEditEmail.innerHTML = "Изменить почту";
        buttonConfEditEmail.className = "buttonConfEdit text-default";

        divAllInputEmail.appendChild(formAllInputEmail);
        formAllInputEmail.appendChild(inputEditEmail1);
        formAllInputEmail.appendChild(firstBrEmail);
        formAllInputEmail.appendChild(inputEditEmail2);
        formAllInputEmail.appendChild(secondBrEmail);
        formAllInputEmail.appendChild(buttonConfEditEmail);
        currentAmount++;

        buttonConfEditEmail.onclick = function () {
            if (inputEditEmail1.value == "" || inputEditEmail2.value == "") {
                return;
            } else {
                let newEmailEdit = inputEditEmail2.value;
                if (inputEditEmail1.value == passwordAccountUser && newEmailEdit.length > 12) {
                    divAllInputEmail.remove();

                    let changeEmail = document.getElementById("menuDBCLEmail");

                    changeEmail.innerHTML = newEmailEdit[0] + newEmailEdit[1] + newEmailEdit[2] + "***@" + newEmailEdit.split("@")[1];
                    currentAmount = 0;

                } else {
                    inputEditEmail1.placeholder = "Пароль неверный";
                    inputEditEmail1.value = "";
                    inputEditEmail2.value = "";
                }
            }

        }
    }

}
