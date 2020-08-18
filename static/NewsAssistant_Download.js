// NewsAssistant_Download.js
// function downloadData() {
// 	var entry = {
// 		data = download_data
// 	};

// 	fetch(`${window.origin}/log/news-assistant-download`, {
// 		method: "POST",
// 		credentials: "include",
// 		body: JSON.stringify(entry),
// 		cache: "no-cache",
// 		headers: new Headers({
// 			"content-type": "application/json"
// 		})
// 		})
// 		.then(function(response) {
// 		if (response.status !== 200) {
// 			console.log(`Looks like there was a problem. Status code: ${response.status}`);
// 			return;
// 		}
// 		response.json().then(function(data) {
// 			console.log(data);
// 		});
// 		})
// 		.catch(function(error) {
// 		console.log("Fetch error: " + error);
// 	});
// }