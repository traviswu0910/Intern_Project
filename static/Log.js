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

function hide(ele) {
	ele.classList.add('hide');
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


function checkBlanks() {
	var notes = getClass('log-note');
	var kws = getClass('log-keyword');
	for (let i=0; i<notes.length; i++) {
		if (notes[i].innerText=='')
			notes[i].innerText = '-';
	}
	for (let i=0; i<kws.length; i++) {
		if (kws[i].innerText=='')
			kws[i].innerText = '-';
	}
}

function checkDates() {
	var dates = getClass('each-date');
	for (let i=0; i<dates.length; i++) {
		if (dates[i].offsetHeight<100) {
			hide(dates[i]);
		}
	}
}

function cheat() {
	var pfs = getClass('log-portfolio');
	for (let i=0; i<pfs.length; i++) {
		if (pfs[i].innerText=="pph_1") {
			pfs[i].innerText = 'Daily 5% above';
		}
		if (pfs[i].innerText=="pph_2") {
			pfs[i].innerText = 'Daily 5% below';
		}
		if (pfs[i].innerText=="pph_3") {
			pfs[i].innerText = 'Weekly 10% above';
		}
		if (pfs[i].innerText=="pph_4") {
			pfs[i].innerText = 'Weekly 10% below';
		}
		if (pfs[i].innerText=="pph_5") {
			pfs[i].innerText = 'Monthly 5% above';
		}
	}
}

