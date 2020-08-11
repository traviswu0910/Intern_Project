var TEXTAREA_DEFAULT = 'Type something your style~';
var grey = 150;

function pin(ind) {
	get('pinned-'+ind).innerHTML = 'true';
}

function unpin(ind) {
	get('pinned-'+ind).innerHTML = 'false';
}

function pinned(ind) {
	if (get('pinned-'+ind).innerHTML=='true')
		return true;
	else
		return false;
}

// notes -- information block
function lockInfo(ind) {
	get('click-block-'+ind).onmouseover = function(){};
	unpin(ind);
	hideInfo(ind);
}

function unlockInfo(ind) {
	get('click-block-'+ind).onmouseover = function() {
		showInfo(get('click-block-'+ind), ind);
	}
}

function showInfo(ele, ind) {
	var delay = setTimeout(function() {
		extendInfo(ind);
	}, 50);
	ele.onmouseout = function() {clearTimeout(delay); hideInfo(ind);};
}

function hideInfo(ind) {
	get('information-block-'+ind).style.height = px(0);
	get('information-parent-block-'+ind).style.height = px(20);
}

function extendInfo(ind) {
	get('information-block-'+ind).style.height = px(60);
	get('information-parent-block-'+ind).style.height = px(80);
}

function pinInfo(ele, ind) {
	if (pinned(ind)) {
		ele.onmouseover = function() {showInfo(ele, ind);};
		hideInfo(ind);
		unpin(ind);
	} else {
		ele.onmouseover = function(){};
		ele.onmouseout = function(){};
		extendInfo(ind);
		pin(ind);
	}
}

function checkFocus(ele) {
	if (ele.value==TEXTAREA_DEFAULT) {
		ele.value = '';
		ele.style.color = 'black';
	}
}

function checkBlur(ele) {
	if (ele.value=='') {
		ele.value = TEXTAREA_DEFAULT;
		ele.style.color = `rgba(${grey}, ${grey}, ${grey}, 1)`;
	}
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

function overElement(e, ele) {
	let mx = e.clientX;
	let my = e.clientY;
	let min = ele.offsetTop;
	let left = ele.offsetLeft;
	let max = min+ele.offsetHeight;
	let right = left+ele.offsetWidth;
	return (my>min && my<max && mx>left && mx<right);
}

function setNotes() {
	let ele = document.getElementById('userHistory');
	ele.style.width = screen.width;
	var edits = document.getElementsByClassName('edit-button');
	var editBtns = document.getElementsByClassName('editBtn');
	var deletes = document.getElementsByClassName('delete-button');
	var titles = document.getElementsByClassName('note-title');
	var noteMsg = document.getElementsByClassName('note-message');	
	let btnHeight = 16;
	let msgHeight = noteMsg[0].offsetHeight;
	for (let i=0; i<edits.length; i++) {
		let blockHeight = titles[i].offsetHeight/2;
		let h = blockHeight+'px';
		let top = (blockHeight/2-btnHeight/2)+'px';
		edits[i].style.height = h;
		deletes[i].style.height = h;
		editBtns[i*2].style.height = btnHeight+'px';
		editBtns[i*2+1].style.width = btnHeight+'px';
		editBtns[i*2].style.marginTop = top;
		editBtns[i*2+1].style.marginTop = top;
		noteMsg[i].style.marginTop = (blockHeight-msgHeight/2)+'px';
	}


	var notes = document.getElementsByClassName('note-textarea');
	var par = document.getElementsByClassName('note-block');
	for (let i=0; i<notes.length; i++) {
		notes[i].style.height = par[i].offsetHeight+'px';
	}

	var tas = getClass('note-textarea');
	for (let i=0; i<tas.length; i++) {
		if (tas[i].value=='') {
			tas[i].value = TEXTAREA_DEFAULT;
			tas[i].style.color = `rgba(${grey}, ${grey}, ${grey}, 1)`;
		}
	}
}

function setCrosses(crossDim) {
	var crosses = getClass('cross');
	var crossImages = getClass('cross-image');
	for (let i=0; i<crosses.length; i++) {
		let blockHeight = crosses[i].offsetHeight;
		crossImages[i].style.height = px(crossDim);
		crossImages[i].style.width = px(crossDim);
		crossImages[i].style.marginTop = px(blockHeight/2-crossDim/2);
	}
}

function setCross(ind, dim) {
	let cross = get('cross-'+ind);
	let crossImage = get('cross-image-'+ind);
	let blockHeight = cross.offsetHeight;
	crossImage.style.height = px(dim);
	crossImage.style.width = px(dim);
	crossImage.style.marginTop = px(blockHeight/2-dim/2);
}

function allowEdit(ind) {
	let ele = get('note-textarea-'+ind);
	ele.focus();
	ele.setSelectionRange(ele.value.length, ele.value.length);
}

function deleteNote(ele, ind, news) {
	userDeleteNote(news);
	let editBtn = get('edit-button-'+ind);
	let btnBlock = get('buttons-block-'+ind);
	let icon = get('delete-icon-'+ind);
	icon.style.transform = "scale(1.5)";
	icon.style.marginTop = editBtn.offsetHeight-icon.offsetHeight/2+'px';
	ele.style.height = (editBtn.offsetHeight*2)+'px';
	editBtn.style.height = '0px';
	btnBlock.style.position = 'absolute';
	btnBlock.style.right = '0';
	btnBlock.style.width = '100%';
	ele.style.borderRadius = '10px';
	ele.classList.remove('delete-button');
	ele.classList.add('deleted');
	icon.classList.remove('editBtn');
	setInterval(function() {
		if (ind>0)
			hide(get('note-block-'+ind));
		else
			hide(get('story-block-'+ind));
	}, 500);
}

function allowDrop(e) {
	e.preventDefault();
}

function drop(e) {
	e.preventDefault();
	let np = get('note-parent');
	let id = e.dataTransfer.getData('id');
	if (getClass('note-block').length==0) {
		np.appendChild(get(id));
	} else {
		np.insertBefore(get(id), np.firstChild);
	}
	// e.target.appendChild(get(id));
}

function dragStart(e, ind) {
	var crosses = getClass('cross');
	for (let i=0; i<crosses.length; i++) {
		crosses[i].classList.add('hide');
	}
	e.dataTransfer.setData('id', e.target.id);
	e.target.classList.add('fade');
	setTimeout(function() {
		e.target.classList.add('hide');
	}, 100);
}

function dragOver(e, ind) {
}

function dragEnd(e, ind, click) {
	if (overElement(e, get('panel-userNote'))) {
		e.target.classList.remove('fade');
		e.target.classList.remove('hide');
		userDeleteStory(click);
		userNote({'link': click['url'], 'title': click['title']}, click['tab'], '');
		hide(get('click-block-'+ind));
		show(get('note-block-'+ind));
		showInline(get('information-parent-block-'+ind));
		let info = get('information-parent-block-'+ind);
		info.classList.remove('click-information');
		info.classList.add('note-information');
		e.target.style.marginBottom = px(-5);
		e.target.draggable = false;
		setNotes();
	} else {
		e.target.classList.remove('fade');
		e.target.classList.remove('hide');
	}
	
	var crosses = getClass('cross');
	for (let i=0; i<crosses.length; i++) {
		crosses[i].classList.remove('hide');
	}
}

function crossClick(ele, ind, news) {
	ele.style.opacity = 0.8;
	ele.style.width = percent(100);
	setCross(ind, 25);
	setTimeout(function() {
		userDeleteStory(news);
		deleteStory(ele, ind);
	}, 300);
}

function deleteStory(ele, ind) {
	setInterval(function() {
		hide(document.getElementById('story-block-'+ind));
	}, 500);
}

function hide(ele) {
	ele.classList.add('hide');
}

function show(ele) {
	ele.classList.remove('hide');
}

function hideInline(ele) {
	hide(ele);
	ele.classList.remove('inline');
}

function showInline(ele) {
	show(ele);
	ele.classList.add('inline');
}

function red(ele) {
	ele.style.backgroundColor = 'red';
}

function noteEdit(e, i, ele, news) {
	let key = e.keyCode;
	let msg = "Note edited!";
	if (key===13) {
		e.preventDefault();
		if (!e.shiftKey) {
			if (ele.value=='')
				msg = 'You left it blank!';
			else if (ele.value==news['note'])
				msg = 'Note unchanged!';
			else
				userChangeNote(news, ele.value);
			showEditMessage(ele, i, msg);	
		}
	}
}

function showEditMessage(t, i, msg) {
	t.blur();
	let ele = document.getElementById('note-message-'+i);
	get('note-message-text-'+i).innerHTML = msg;
	ele.style.opacity = 1;
	showMsgBlock(i);
	setTimeout( function() {
		ele.style.opacity = 0;
		hideMsgBlock(i);
	}, 1500);

}

function hideMsgBlock(i) {
	document.getElementById('note-message-'+i).style.display = 'none';
}

function showMsgBlock(i) {
	document.getElementById('note-message-'+i).style.display = 'inline-block';
}

function noteInput(e, news, ind, ele) {
	var key = e.keyCode;
	// If the user has pressed enter
	if (key === 13) {
		if (!e.shiftKey) {
			if (ele.value!='') {
				userNote(news, ind, ele.value);
			}
			ele.blur();
			ele.style.display = 'none';
		}	
	}
}

function showNote(i, j) {
	let id = "note-".concat(i, j);
	let x = document.getElementById(id);
	if (x.style.display=='none')
		x.style.display = 'inline-block';
	else
		x.style.display = 'none';
	x.focus();
}

function updateNote(ele, i, news) {
	if (ele.value!='') {
		userNote(news, i, ele.value);
	}
}

function userChangeNote(news, note) {
	var entry = {
		note: note,
		news: news,
	};

	fetch(`${window.origin}/log/news-assistant-change-note`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(entry),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json"
		})
	}).then(function(response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
		response.json().then(function(data) {
			console.log(data);
		});
	}).catch(function(error) {
		console.log("Fetch error: " + error);
	});
}

function userDeleteNote(news) {
	var entry = {
		news: news,
	};

	fetch(`${window.origin}/log/news-assistant-delete-note`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(entry),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json"
		})
	}).then(function(response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
		response.json().then(function(data) {
			console.log(data);
		});
	}).catch(function(error) {
		console.log("Fetch error: " + error);
	});
}

function userDeleteStory(news) {
	var entry = {
		news: news,
	};

	fetch(`${window.origin}/log/news-assistant-delete-story`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(entry),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json"
		})
	}).then(function(response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
		response.json().then(function(data) {
			console.log(data);
		});
	}).catch(function(error) {
		console.log("Fetch error: " + error);
	});
}

function userNote(obj, tab, note) {
	var entry = {
		title: obj['title'],
		url: obj['link'],
		tab: tab,
		note: note,
	};

	fetch(`${window.origin}/log/news-assistant-note`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(entry),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json"
		})
		})
		.then(function(response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
		response.json().then(function(data) {
			console.log(data);
		});
		})
		.catch(function(error) {
		console.log("Fetch error: " + error);
	});
}

function userClick(obj, tab) {
	var entry = {
		title: obj['title'],
		url: obj['link'],
		tab: tab,
	};

	fetch(`${window.origin}/log/news-assistant-click`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(entry),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json"
		})
		})
		.then(function(response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
		response.json().then(function(data) {
			console.log(data);
		});
		})
		.catch(function(error) {
		console.log("Fetch error: " + error);
	});
}

function openTab(tabName) {
	var i;
	var x = document.getElementsByClassName("bottompane-tabs");
	for (i = 0; i < x.length; i++) {
		x[i].style.display = "none";	
	}
	document.getElementById(tabName).style.display = "block";	
}


// chart
function drawChart(r) {
	var ret = r;
	var companies = [];
	var bgColor = [
		'rgba(255, 206, 86, 0.2)',
		'rgba(75, 192, 192, 0.2)',
		'rgba(153, 102, 255, 0.2)',
		'rgba(255, 159, 64, 0.2)',
	];
	var bdColor = [
		'rgba(255, 206, 86, 1)',
		'rgba(75, 192, 192, 1)',
		'rgba(153, 102, 255, 1)',
		'rgba(255, 159, 64, 1)',
	];
	var count=0;
	ret.forEach(
		(company) => {
			var r = Math.floor(Math.random()*256);
			var g = Math.floor(Math.random()*256);
			var b = Math.floor(Math.random()*256);
			companies.push({
				label: company['company'],
				data: [
					company['day'],
					company['week'],
					company['month'],
					company['year']
				], 
				backgroundColor: `rgba(${r}, ${g}, ${b}, 0.2)`,
				borderColor: `rgba(${r}, ${g}, ${b}, 1)`,
				borderWidth: 1,
				hidden: true,
			});
			count++;
		}
	);
	var ctx = document.getElementById('myChart');
	var myChart = new Chart(ctx, {
		type: 'bar',
		data: {
			// hidden=true,
			labels: ['Day', 'Week', 'Month', 'Year'],
			datasets: companies,
		},
		options: {
			layout: {
				padding: {
					top: -45,
				},
			},
			title: {
				display: true,
				text: 'Annualized Return',
				fontSize: 38,
			},
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: true,
						fontColor: 'white'
					}
				}],
				xAxes: [{
					ticks: {
						fontColor: 'white',

					}
				}]
			},
			legend: {
				labels: {
					fontColor: 'white',
				},
			},
		},
		// hidden=true
	});
}




