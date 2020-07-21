function fillInfo(username, password, retype) {
	document.getElementById("input_usr").value = username;
	document.getElementById("input_pwd").value = password;
	document.getElementById("input_retype").value = retype;
}

function checkRetype(r) {
	if (r==1) {
		document.getElementById("input_retype").style.display = "block"; 
	}
}

function setTogo(utils) {
	for (let i=0; i<utils.length; i++) {
		let id = utils[i]['id'];
		item = document.getElementById(id);
		item.name = id;
		item.value = "0";
	}
}

function utilClick(ele, utils) {
	if (!ele.classList.contains("togo-icon-clicked")) {
		for (let i=0; i<utils.length; i++) {
			let id = utils[i].id;
			if (id!=ele.id) {
				let item = document.getElementById(id);
				item.classList.remove("togo-icon-clicked");
				document.getElementById(id.concat('_input')).value = '0';
			}
		}
		ele.classList.add("togo-icon-clicked");
		document.getElementById(ele.id.concat('_input')).value = '1';
	} else {
		ele.classList.remove("togo-icon-clicked");
		document.getElementById(ele.id.concat('_input')).value = '0';
	}
}