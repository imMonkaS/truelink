let limitN = 1;
let currentAmountN = 0;

document.getElementById("NameValue").onclick = function () {
    if (currentAmountN < limitN) {
        let firstName = document.getElementById("FirstName").innerHTML;
        let lastName = document.getElementById("LastName").innerHTML;
        let elemName = document.getElementById('EditName');
        let oldDivEditLink = document.createElement("div");
        oldDivEditLink.className = "settTextDiv";
        
        elemName.appendChild(oldDivEditLink);
        
        let inputName = document.createElement("input");
        inputName.value = firstName;
        inputName.className = "editValue text-default";
        
        let inputLastName = document.createElement("input");
        inputLastName.value = lastName;
        inputLastName.className = "editValue text-default";

        let buttonName = document.createElement("button");
        buttonName.className = "buttonConfEdit text-default";
        buttonName.innerHTML = "Изменить имя";
        
        oldDivEditLink.appendChild(inputName);
        oldDivEditLink.appendChild(inputLastName);
        oldDivEditLink.appendChild(buttonName);
        currentAmountN++;

        buttonName.onclick = function () {
            if (inputName.value == "" || inputLastName.value == ""){
                return;
            }
            let newName = inputName.value;
            let newLastName = inputLastName.value;
            oldDivEditLink.remove()

            document.getElementById("FirstName").innerHTML = newName;
            document.getElementById("LastName").innerHTML = newLastName;

            currentAmountN = 0;
        }
    }


}
