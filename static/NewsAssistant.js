// function pickDate(){
//     this.datepicker();
//     // <!--$("#datepicker").datepicker("setDate", new Date());-->
// };

// function process(e, a, b, c) {
// 	var k = e.keyCode;
// 	if (k==13) {
// 		alert("Success!");
// 	}
// }


$(function() {
	$('.lazy').lazy();
});

function noteInput(e, news, i, j) {
	var key = e.keyCode;
	let id = "note-".concat(i, j);
	// If the user has pressed enter
	if (key === 13) {
		if (!e.shiftKey) {
			x = document.getElementById(id);
			note = x.value;
			userNote(news, i, note);
			x.style.display = 'none';
		}	
	}
}

function showNote(i, j) {
	let id = "note-".concat(i, j);
	let x = document.getElementById(id);
	if (x.style.display==='none')
		x.style.display = 'inline-block';
	else
		x.style.display = 'none';
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




