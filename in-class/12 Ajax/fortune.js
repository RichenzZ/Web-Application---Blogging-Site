var req;

function sendRequest(){
	if(window.XMLHttpRequest){
		req = new XMLHttpRequest();
	}
	else{
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	req.onreadystatechange = getFortune;
	req.open("GET", "https://garrod.isri.cmu.edu/webapps/fortune/", true);
	req.send();

}
function getFortune() {
	console.log(req);
	if(req.readyState != 4 || req.status != 200){
		return;
	}
	var content = document.getElementById("content");
	var items = JSON.parse(req.responseText);
	var text = items["fortune"];
	var newitem = document.createElement("p");
	newitem.innerHTML = text;
	content.append(newitem);
}

// window.setInterval(sendRequest, 10000);
