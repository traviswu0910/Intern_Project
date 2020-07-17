
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