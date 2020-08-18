// Log.js

var logHeights = {};

function parentClass(ele, className) {
	while(!ele.classList.contains(className))
		ele = ele.parentNode;
	return ele;
}

function px(t) {
	return t+'px';
}

function percent(x) {
	return x+'%';
}

function get(id) {
	return document.getElementById(id);
}

function getClass(name) {
	return document.getElementsByClassName(name);
}

function recordLogHeights() {
	var logs = getClass('log-parent');
	for (let i=0; i<logs.length; i++) {
		logHeights[logs[i].id] = logs[i].offsetHeight;
	}
}

function setLogHeights() {
	var logs = getClass('log-parent');
	for (let i=0; i<logs.length; i++) {
		logs[i].style.height = px(logHeights[logs[i].id]);
	}
}

function dateClick(ind) {
	let date = get(ind);
	if (date.offsetHeight>5) {
		date.style.height = px(0);
		date.style.marginBottom = px(-20);
	} else {
		date.style.height = px(logHeights[ind]);
		date.style.marginBottom = px(10);
	}
}


