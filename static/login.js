
function fillInfo(refill, username, password) {
	if (refill==1) {
		document.getElementById("input_usr").value = username;
		document.getElementById("input_pwd").value = password;
	}
}

function checkRetype(r) {
	if (r==1) {
		document.getElementById("retype").style.display = "block"; 
	}
}