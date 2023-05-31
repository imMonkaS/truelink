let passwordAccountUserPh = "123"; // Значение берем из ДБ
let limitPh = 1;
let currentAmountPh = 0;

spanEditorPhone.onclick = function () {
    if (currentAmountPh < limitPh) {
        let elemphone = document.getElementById('phoneForm');
        let divAllInputPhone = document.createElement("div");
        divAllInputPhone.className = "settTextDiv";
        elemphone.appendChild(divAllInputPhone);

        let formAllInputPhone = document.createElement("form");
        divAllInputPhone.appendChild(formAllInputPhone);

        let inputEditPhone1 = document.createElement("input");
        inputEditPhone1.className = "editValue settingEditorInput text-default";
        inputEditPhone1.placeholder = "Введите пароль";
        inputEditPhone1.type = "password";
        inputEditPhone1.setAttribute("required", "");

        let firstBrPhone = document.createElement("br");

        let inputEditPhone2 = document.createElement("input");
        inputEditPhone2.className = "editValue settingEditorInput text-default";
        inputEditPhone2.placeholder = "Номер телефона";
        inputEditPhone2.type = "tel";
        inputEditPhone2.setAttribute("required", "");

        let secondBrPhone = document.createElement("br");

        let buttonConfEditPhone = document.createElement("button");
        buttonConfEditPhone.innerHTML = "Изменить телефон";
        buttonConfEditPhone.className = "buttonConfEdit text-default";
        
        formAllInputPhone.appendChild(inputEditPhone1);
        formAllInputPhone.appendChild(firstBrPhone);
        formAllInputPhone.appendChild(inputEditPhone2);
        formAllInputPhone.appendChild(secondBrPhone);
        formAllInputPhone.appendChild(buttonConfEditPhone);
        
        currentAmountPh++;

        buttonConfEditPhone.onclick = function () {
            if (inputEditPhone1.value == "" || inputEditPhone2.value == "") {
                return;
            } else {
                if (inputEditPhone1.value == passwordAccountUserPh) {
                    divAllInputPhone.remove();

                    let editPhone = document.getElementById("menuDBCLPhone");

                    editPhone.innerHTML = inputEditPhone2.value;
                    currentAmountPh = 0;

                } else {
                    inputEditPhone1.placeholder = "Пароль неверный";
                    inputEditPhone1.value = "";
                    inputEditPhone2.value = "";
                }
            }
        }
    }

}
