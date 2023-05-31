document.write('<script src="http://' + (location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1"></' + 'script>');

// Пароль

let passwordAccountUser = "123"; // Значение берем из ДБ

passwordSetting.onclick = function(){
	passwordSetting.remove();

	let elem = document.getElementById('passwordForm');
	let divAllInput = document.createElement("div");
	divAllInput.className = "settTextDiv";
	elem.appendChild(divAllInput);

	let formAllInput = document.createElement("form");
	divAllInput.appendChild(formAllInput);

	let inputEditPass1 = document.createElement("input");
	inputEditPass1.className = "editValue settingEditorInput";
	inputEditPass1.placeholder = "Введите ваш пароль";
	inputEditPass1.type = "password";
	inputEditPass1.id = "inputTruePassword1";
	inputEditPass1.setAttribute("required", "");
	formAllInput.appendChild(inputEditPass1);

	let firstBr1 = document.createElement("br");
	formAllInput.appendChild(firstBr1);

	let inputEditPass2 = document.createElement("input");
	inputEditPass2.className = "editValue settingEditorInput";
	inputEditPass2.placeholder = "Введите новый пароль";
	inputEditPass2.type = "password";
	inputEditPass2.id = "inputTruePassword2";
	inputEditPass2.setAttribute("required", "");
	formAllInput.appendChild(inputEditPass2);

	let firstBr2 = document.createElement("br");
	formAllInput.appendChild(firstBr2);

	let inputEditPass3 = document.createElement("input");
	inputEditPass3.className = "editValue settingEditorInput";
	inputEditPass3.placeholder = "Введите новый пароль";
	inputEditPass3.type = "password";
	inputEditPass3.id = "inputTruePassword3";
	inputEditPass3.setAttribute("required", "");
	formAllInput.appendChild(inputEditPass3);

	let buttonCofirmEditPass = document.createElement("button");
	buttonCofirmEditPass.className = "buttonConfEdit";
	buttonCofirmEditPass.innerHTML = "Изменить пароль";
	buttonCofirmEditPass.id = "buttonConfEditPass";
	formAllInput.appendChild(buttonCofirmEditPass);

	buttonCofirmEditPass.onclick = function() {
		if (inputEditPass1.value == "" || inputEditPass2.value == "" || inputEditPass3.value == "") {
			return;
		}
		else {
			if(inputEditPass1.value == passwordAccountUser){
				if (inputEditPass2.value == inputEditPass3.value) {
					divAllInput.remove();

					//////////////////////////

					let oldDivEditPass = document.createElement("div");
					oldDivEditPass.className = "settTextDiv";
					oldDivEditPass.id = "paswordSetting";
					elem.appendChild(oldDivEditPass);

					let oldSpanEditPass = document.createElement("span");
					oldSpanEditPass.className = "settTextSett";
					oldSpanEditPass.id = "menuDBCLPassword";
					oldSpanEditPass.innerHTML = "Был изменен только что";
					oldDivEditPass.appendChild(oldSpanEditPass);

					let oldSpan2EditPass = document.createElement("span");
					oldSpan2EditPass.className = "settTextBut";
					oldSpan2EditPass.id = "spanEditorPassword";
					oldSpan2EditPass.innerHTML = "Изменить";
					oldDivEditPass.appendChild(oldSpan2EditPass);
				}
				else {
					inputEditPass2.placeholder = "Пароли различаются";
					inputEditPass3.placeholder = "Пароли различаются";
					inputEditPass1.value = "";
					inputEditPass2.value = "";
					inputEditPass3.value = "";
				}
			}
			else {
				inputEditPass1.placeholder = "Пароль неправильный";
				inputEditPass1.value = "";
				inputEditPass2.value = "";
				inputEditPass3.value = "";
			}
		}
	}
}


// Почта


emailSetting.onclick = function() {
	emailSetting.remove();


	let elem = document.getElementById('emailForm');
	let divAllInputEmail = document.createElement("div");
	divAllInputEmail.className = "settTextDiv";
	elem.appendChild(divAllInputEmail);

	let formAllInputEmail = document.createElement("form");
	divAllInputEmail.appendChild(formAllInputEmail);

	let inputEditEmail1 = document.createElement("input");
	inputEditEmail1.className = "editValue settingEditorInput";
	inputEditEmail1.placeholder = "Введите пароль";
	inputEditEmail1.type = "password";
	inputEditEmail1.setAttribute("required", "");
	formAllInputEmail.appendChild(inputEditEmail1);

	let firstBrEmail = document.createElement("br");
	formAllInputEmail.appendChild(firstBrEmail);

	let inputEditEmail2 = document.createElement("input");
	inputEditEmail2.className = "editValue settingEditorInput";
	inputEditEmail2.placeholder = "Введите новую почту";
	inputEditEmail2.type = "email";
	inputEditEmail2.setAttribute("required", "");
	formAllInputEmail.appendChild(inputEditEmail2);

	let secondBrEmail = document.createElement("br");
	formAllInputEmail.appendChild(secondBrEmail);

	let buttonConfEditEmail = document.createElement("button");
	buttonConfEditEmail.innerHTML = "Изменить почту";
	buttonConfEditEmail.className = "buttonConfEdit";
	buttonConfEditEmail.id = "buttonConfEditEmail";
	formAllInputEmail.appendChild(buttonConfEditEmail);

	buttonConfEditEmail.onclick = function() {
		if(inputEditEmail1.value == "" || inputEditEmail2.value == ""){
			return;
		}
		else {
			let newEmailEdit = inputEditEmail2.value;
			if(inputEditEmail1.value == passwordAccountUser && newEmailEdit.length > 12){
				divAllInputEmail.remove();

				///////////////////////////

				let oldDivEditEmail = document.createElement("div");
				oldDivEditEmail.className = "settTextDiv";
				oldDivEditEmail.id = "emailSetting";
				elem.appendChild(oldDivEditEmail);

				let oldSpanEditEmail = document.createElement("span");
				oldSpanEditEmail.className = "settTextSett";
				oldSpanEditEmail.id = "menuDBCLEmail";
				oldSpanEditEmail.innerHTML = newEmailEdit[0] + newEmailEdit[1] + newEmailEdit[2];
				oldSpanEditEmail.innerHTML += "***@";
				oldSpanEditEmail.innerHTML += newEmailEdit.split("@")[1];
				oldDivEditEmail.appendChild(oldSpanEditEmail);

				let oldSpan2EditEmail = document.createElement("span");
				oldSpan2EditEmail.className = "settTextBut";
				oldSpan2EditEmail.id = "spanEditorEmail";
				oldSpan2EditEmail.innerHTML = "Изменить";
				oldDivEditEmail.appendChild(oldSpan2EditEmail);
			}
			else {
				inputEditEmail1.placeholder = "Пароль неверный";
				inputEditEmail1.value = "";
				inputEditEmail2.value = "";
			}
		}

	}
}


// Телефон


phoneSetting.onclick = function() {
	menuDBCLPhone.remove();
	spanEditorPhone.remove();
	phoneSetting.remove();

	let elemphone = document.getElementById('phoneForm');
	let divAllInputPhone = document.createElement("div");
	divAllInputPhone.className = "settTextDiv";
	elemphone.appendChild(divAllInputPhone);

	let formAllInputPhone = document.createElement("form");
	divAllInputPhone.appendChild(formAllInputPhone);

	let inputEditPhone1 = document.createElement("input");
	inputEditPhone1.className = "editValue settingEditorInput";
	inputEditPhone1.placeholder = "Введите пароль";
	inputEditPhone1.type = "password";
	inputEditPhone1.setAttribute("required", "");
	formAllInputPhone.appendChild(inputEditPhone1);

	let firstBrPhone = document.createElement("br");
	formAllInputPhone.appendChild(firstBrPhone);

	let inputEditPhone2 = document.createElement("input");
	inputEditPhone2.className = "editValue settingEditorInput";
	inputEditPhone2.placeholder = "Введите телефон";
	inputEditPhone2.type = "tel";
	inputEditPhone2.setAttribute("required", "");
	formAllInputPhone.appendChild(inputEditPhone2);

	let secondBrPhone = document.createElement("br");
	formAllInputPhone.appendChild(secondBrPhone);

	let buttonConfEditPhone = document.createElement("button");
	buttonConfEditPhone.innerHTML = "Изменить телефон";
	buttonConfEditPhone.className = "buttonConfEdit";
	buttonConfEditPhone.id = "buttonConfEditPhone";
	formAllInputPhone.appendChild(buttonConfEditPhone);

	buttonConfEditPhone.onclick	 = function() {
		if(inputEditPhone1.value == "" || inputEditPhone2.value == ""){
			return;
		}
		else {
			if (inputEditPhone1.value == passwordAccountUser) {
				divAllInputPhone.remove();

				let oldDivEditPass = document.createElement("div");
				oldDivEditPass.className = "settTextDiv";
				oldDivEditPass.id = "phoneSetting";
				elemphone.appendChild(oldDivEditPass);

				let oldSpanEditPass = document.createElement("span");
				oldSpanEditPass.className = "settTextSett";
				oldSpanEditPass.id = "menuDBCLPhone";
				oldSpanEditPass.innerHTML = "+7 977 645 85 30"
				oldDivEditPass.appendChild(oldSpanEditPass);

				let oldSpan2EditPass = document.createElement("span");
				oldSpan2EditPass.className = "settTextBut";
				oldSpan2EditPass.id = "spanEditorPhone";
				oldSpan2EditPass.innerHTML = "Изменить";
				oldDivEditPass.appendChild(oldSpan2EditPass);
			}
			else {
				inputEditPhone1.placeholder = "Пароль неверный";
				inputEditPhone1.value = "";
				inputEditPhone2.value = "";
			}
		}
	}
}


// Ссылка


let linkUser = "testDemo"; // Берем его ссылку


linkSetting.onclick = function() {
	linkSetting.remove();

	let elemLink = document.getElementById('linkForm');
	let oldDivEditLink = document.createElement("div");
	oldDivEditLink.className = "settTextDiv";
	elemLink.appendChild(oldDivEditLink);

	let oldSpanEditLink = document.createElement("span");
	oldSpanEditLink.className = "grayHTTPS spanLink";
	oldSpanEditLink.innerHTML = "https://truelink.com/";
	oldDivEditLink.appendChild(oldSpanEditLink);

	let inputEditLink = document.createElement("input");
	inputEditLink.className = "editValue settingEditorInput inputLink";
	inputEditLink.value = linkUser;
	inputEditLink.maxlength = "32";
	oldDivEditLink.appendChild(inputEditLink);

	let buttonCofirmEditLink = document.createElement("button");
	buttonCofirmEditLink.className = "buttonConfEdit";
	buttonCofirmEditLink.id = "buttonConfirmEditPhone";
	buttonCofirmEditLink.innerHTML = "Изменить ссылку";
	oldDivEditLink.appendChild(buttonCofirmEditLink);

	buttonCofirmEditLink.onclick = function() {
		if (inputEditLink.value != "") {
			let userNewLink = inputEditLink.value;
			oldDivEditLink.remove();

			let oldNewDivEditLink = document.createElement("div");
			oldNewDivEditLink.className = "settTextDiv";
			oldNewDivEditLink.id = "linkSetting";
			elemLink.appendChild(oldNewDivEditLink);

			let oldSpanEditLink = document.createElement("span");
			oldSpanEditLink.className = "settTextSett";
			oldNewDivEditLink.appendChild(oldSpanEditLink);

			let oldSpanEditTrueLink = document.createElement("span");
			oldSpanEditTrueLink.className = "grayHTTPS";
			oldSpanEditTrueLink.innerHTML = "https://truelink.com/";
			oldSpanEditLink.appendChild(oldSpanEditTrueLink);

			let oldSpanEditUserLink = document.createElement("span");
			oldSpanEditUserLink.className = "normHTTPS";
			oldSpanEditUserLink.id = "menuDBCLAdres";
			oldSpanEditUserLink.innerHTML = userNewLink;
			oldSpanEditLink.appendChild(oldSpanEditUserLink);

			let oldSpan2EditPass = document.createElement("span");
			oldSpan2EditPass.className = "settTextBut";
			oldSpan2EditPass.id = "spanEditorLink";
			oldSpan2EditPass.innerHTML = "Изменить";
			oldNewDivEditLink.appendChild(oldSpan2EditPass);
		}
	}
}


// Демо-страничка


nameSpanToInp.onclick = function() {
	let nameEdit = nameSpanToInp.innerHTML;
	nameSpanToInp.remove();

	let elem = document.getElementById('name');
	let inputCreateEdit = document.createElement("input");
	inputCreateEdit.value = nameEdit;
	inputCreateEdit.className = "editValue";
	inputCreateEdit.id = "newInputEdit";
	elem.appendChild(inputCreateEdit);



	inputCreateEdit.onkeyup = function(e) {
		if (e.keyCode == 13) {
	        let newNameInp = inputCreateEdit.value;
	        inputCreateEdit.remove()

	        let elem2 = document.getElementById('name');;
	        let oldSpanEdit = document.createElement("span");
	     	oldSpanEdit.innerHTML = newNameInp;
	    	oldSpanEdit.className = "demoName";
	    	oldSpanEdit.id = "nameSpanToInp";
	    	elem2.appendChild(oldSpanEdit);
	    }
	}
}
