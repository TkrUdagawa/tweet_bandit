var ws = new WebSocket("ws://localhost:9000/ws");

ws.onopen = function() {
    ws.send(JSON.stringify({"type":"init"})); 
};

ws.onmessage = function (evt) {
    var j = JSON.parse(evt.data);
    if (j["type"] == "select") {
        elem=document.getElementById("layer1");
        var childNodes = elem.childNodes, i = childNodes.length;
        while (i--) {
            elem.removeChild(childNodes[i]);
        }
        console.log(j["data"]);
        show_arms(elem, j["data"]);
        status_layer = document.getElementById("status");
        status_layer.innerHTML = "";
    }
    else if (j["type"] == "display") {
	display_arm(j["arm_info"]);
    }
};

function display_arm(arm_js) {
    arm_info_layer=document.getElementById("display_arm_info");
    var childNodes = arm_info_layer.childNodes, i = childNodes.length;

    while (i--) {
        arm_info_layer.removeChild(childNodes[i]);
    }
    i = 0 
    for (category in arm_js) {
	trial_count_list = []
	weight_list = [] 
	arm_list = []
	var chart = document.createElement("span")
	chart.style = "POSITION:absolute; LEFT:" + String(i * 500)
	i += 1
	arm_info_layer.appendChild(chart);
	chart.id = "arm_info_" + category
        console.log("display_arm")
	for (arm_id in arm_js[category]) {
	    weight = parseFloat(arm_js[category][arm_id]["weight"])
	    trial_count = parseFloat(arm_js[category][arm_id]["trial_count"]) - weight
	    arm_list.push(arm_id)
	    trial_count_list.push([arm_list.length, trial_count]);	    
	    weight_list.push([arm_list.length, weight]);
	}

	jQuery . jqplot(
	    chart.id,
            [
		weight_list, trial_count_list
            ],
            {
		stackSeries: true,
		title:chart.id,
		seriesDefaults: {
                    renderer: jQuery . jqplot . BarRenderer,
		    
		},
		axesDefaults: {
		    tickRenderer: jQuery . jqplot . CanvasAxisTickRenderer,
		    tickOptions: {
			angle: -45,
		    }
		},
		axes: {
                    xaxis: {
			renderer: jQuery . jqplot . CategoryAxisRenderer,
			ticks:arm_list,
                    }
		}
            }
	);
    }
    console.log(arm_js);
}

function show_loading() {
    elem = document.getElementById("status");
    elem.innerHTML = '<img src = "static/img/loading.gif">';
}

function select_arm() {
    tweet_num = document.forms.bandit.tweet_num.value;
    console.log(tweet_num);
    ws.send(JSON.stringify({"type":"select", "tweet_num":tweet_num}));
    show_loading();
};

function reset_arm() {
    console.log("reset arms");
    ws.send(JSON.stringify({"type":"reset"}));
}

function display_arm_info() {
    console.log("display_arm");
    ws.send(JSON.stringify({"type":"display_arm"}));
}

function save_model() {
    console.log("save models");
    ws.send(JSON.stringify({"type":"save"}));
}

function show_arms(parent, json_data) {
    var tbl = document.createElement("table")
    for (result_id in json_data) {
        category = json_data[result_id]["category"];
        user = json_data[result_id]["user"];
        text = json_data[result_id]["text"];
        img_src = json_data[result_id]["img_src"];
        user_url = json_data[result_id]["user_url"];
	
        var tr = document.createElement("tr");
        tr.id = "tweet" + result_id;
        tr.setAttribute("userid", user);
        tr.setAttribute("category", category);
	
        // create a first column item
        td_category = document.createElement("td");
        td_category.innerHTML = category;
	
        // create a second column item
        td_img = document.createElement("td");
        td_img.innerHTML = '<img src = "' +  img_src + '">';
	
        // create a third column item
        td_tweet = document.createElement("td");
        td_tweet.id = "tweet_body" + result_id;
        td_tweet.innerHTML = '<a href ="' + user_url + '" target = "_blank">@' + user + '<br>';
	td_tweet.innerHTML += text.replace(/((http:|https:)\/\/[\x21-\x26\x28-\x7e]+)/gi, "<a href='$1' target='_blank'>$1</a>");
	
	tr.appendChild(td_category);
	tr.appendChild(td_img);
        tr.appendChild(td_tweet);
        tbl.appendChild(tr);
    }
    
    parent.appendChild(tbl);
    
    $("table tr").on("click", function(){
        console.log($(this));
        var userid =  $(this)[0].getAttribute("userid");
	var category = $(this)[0].getAttribute("category");
        ws.send(JSON.stringify({"type":"update", "user":userid, "category":category}));
        $(this)[0].setAttribute("userid", "");
        $(this)[0].setAttribute("category", "");
        $(this).css({"color": "gray"});
    })
    
    $("table tr").on("mouseenter", function() {
        $(this).css({"background-color": "#ddd"});
    })
    
    $("table tr").on("mouseleave", function() {
        $(this).css({"background-color": "white"});
    })
};

