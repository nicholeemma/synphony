
var webSocket = new WebSocket('ws://' + window.location.host + '/ws/sync' + window.location.pathname);


$(document).ready(function(){

	var isHost = $("#music-bar").attr("data-isHost")

	if(isHost === "True") { process_host(); }

});


function start_playing(cur) {

	var isHost = $("#music-bar").attr("data-isHost")

	if(isHost === "False") { 

		if ($(cur).html() === "Start"){
			process_participant(webSocket);
			document.getElementById('music-bar').muted = false;
			$(cur).html("Stop");
		} else if ($(cur).html() === "Stop") {
			document.getElementById('music-bar').muted = true;
			$(cur).html("Start");
		}
	 
	}
}


function process_host(){

	$("#music-bar").bind("seeked", function() {
		var cur_time = $("#music-bar")[0].currentTime;
		webSocket.send(JSON.stringify({
			'msg_type' : 'seeked_time', 'msg_content': cur_time
		}));
	});

	$("#music-bar").bind("loadstart", function() {
		var cur_src = $("#audiosrc").attr("src");
		webSocket.send(JSON.stringify({
			'msg_type' : 'loadstart_src', 'msg_content': cur_src
		}));
	});

	$("#music-bar").bind("pause", function() {
		webSocket.send(JSON.stringify({
			'msg_type' : 'play_status', 'msg_content': 'pause'
		}));
	});

	$("#music-bar").bind("playing", function() {
		webSocket.send(JSON.stringify({
			'msg_type' : 'play_status', 'msg_content': 'play'
		}));
	});

	$("#music-bar").bind("volumechange", function() {
		var volume = $("#music-bar")[0].volume;
		webSocket.send(JSON.stringify({
			'msg_type' : 'volume_change', 'msg_content': volume
		}));
	});

	webSocket.onmessage = function(e) {

		var data = JSON.parse(e.data);
		var msg_type = data['msg_type'];
			
		if (msg_type === 'sync_all_request')
		{
			var volume = $("#music-bar")[0].volume;
			var is_paused = $("#music-bar")[0].paused;
			var cur_time = $("#music-bar")[0].currentTime;
			var cur_src = $("#audiosrc").attr("src");

			webSocket.send(JSON.stringify({
				'msg_type' : 'sync_all_response', 
				'msg_content': {
					'volume' : volume,
					'is_paused' : is_paused,
					'cur_time' : cur_time, 
					'cur_src' : cur_src
				}
			}));
		}

	}
}

function process_participant(){

	
	if (webSocket.readyState === WebSocket.OPEN) {
		webSocket.send(JSON.stringify(
			{ 'msg_type' : 'sync_all_request', 'msg_content': 'None' }));
	}

	webSocket.onmessage = function(e) {

		var data = JSON.parse(e.data);
		var msg_type = data['msg_type'];
		var msg_content = data['msg_content'];

		if (msg_type === 'loadstart_src') {

			$("#audiosrc").attr("src", msg_content);
			document.getElementById('music-bar').load();
			document.getElementById('music-bar').play();

		} else if (msg_type === 'seeked_time') {

			$("#music-bar")[0].currentTime = msg_content;

		} else if (msg_type === 'play_status') {

			if (msg_content == 'play') {
				document.getElementById('music-bar').play();
			} else if (msg_content == 'pause') {
				document.getElementById('music-bar').pause();
			}

		} else if (msg_type === 'volume_change') {

			$("#music-bar")[0].volume = msg_content;

		} else if (msg_type === 'sync_all_response') {

			var volume = msg_content['volume'];
			var is_paused = msg_content['is_paused'];
			var cur_time = msg_content['cur_time'];
			var cur_src = msg_content['cur_src'];

			if ($("#audiosrc").attr("src") !== cur_src) {
				$("#audiosrc").attr("src", cur_src);
				document.getElementById('music-bar').load();
				document.getElementById('music-bar').play();

				$("#music-bar")[0].currentTime = cur_time;
				$("#music-bar")[0].volume = volume;
				$("#music-bar")[0].paused = is_paused;
			}

		} else if (msg_type === 'close_studio' && webSocket.readyState === WebSocket.OPEN) {

			document.getElementById('music-bar').pause();
			document.getElementById('music-bar').muted = true;

			$('#start-btn').html("The studio has been closed.");
			document.getElementById('start-btn').disabled = true;

			webSocket.close();

		}
	};
}

function close_studio() {
	alert("Studio is closing");

	var isHost = $("#music-bar").attr("data-isHost")

	if(isHost === "True" && webSocket.readyState === WebSocket.OPEN) { 

		document.getElementById('music-bar').pause();
		document.getElementById('music-bar').muted = true;

		$('#close-btn').html("The studio has been closed.");
		document.getElementById('close-btn').disabled = true;

		webSocket.send(JSON.stringify({
			'msg_type' : 'close_studio', 'msg_content': "None"
		}));

		webSocket.close();

	}	
}