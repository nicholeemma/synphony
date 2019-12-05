// web socket js for playlist
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var webSocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + '/ws/playlist' + window.location.pathname);

$(function () {
    console.log("playlist.js loaded!");
});


$(document).ready(function(){

    var isHost = $("#music-bar").attr("data-isHost")

    if(isHost === "True") { process_host(); }

    process_participant()

});


function process_host(){
    //bind add songs
    //here the button is bind twice(somewhere, unbind them first)
    $("[name='song-name-add']").unbind("click").bind("click", function () {
        var song_id = $(this)["0"].value
        // get music file url
        var url = "https://api.imjad.cn/cloudmusic/?type=song&id=" + song_id
        var json_obj = JSON.parse(Get(url));
        var musicUrl = json_obj["data"][0]["url"];

        //get song info, example
            //["Hello", " by: 王霏霏（Fei）/ 王嘉尔  Add"]
            // 0: "Hello"
            // 1: " by: 王霏霏（Fei）/ 王嘉尔  Add"
        var object = document.getElementById(song_id);
        var song_info = object.textContent;
        var name = song_info.split(',')[0];
        var description = song_info.split(',')[1];
        var data = {};
        data['name'] = name;
        data['description'] = description;
        data['url'] = musicUrl;
        console.log("add songs sent!")
        webSocket.send(JSON.stringify({
            'msg_type': 'add_song',
            'msg_content': data,
        }));
    })

    //bind remove songs when page is opened
    $("[name='remove_song']").bind("click", function(){
        console.log('delete song js triggered!');
        var musicId  =  $(this)["0"].value;
        var data = {'id': musicId};
        console.log("remove songs sent!")
        webSocket.send(JSON.stringify({
            'msg_type': 'remove_song',
            'msg_content': data,
        }));
        $(this).parents()[1].remove();
    })


    webSocket.onmessage = function(e){
        var data = JSON.parse(e.data);
        var msg_type = data['msg_type'];
        var msg_content = data['msg_content']

        if ('error' in msg_content) {
            alert("Error: " + msg_content['error']);
		} else if (msg_type === 'add_song'){
        }
    }
}


function process_participant(){

    webSocket.onmessage = function(e) {
        var isHost = $("#music-bar").attr("data-isHost")
        var data = JSON.parse(e.data);
        var msg_type = data['msg_type'];
        var msg_content = data['msg_content'];

        //add songs
        if ('error' in msg_content){
            if(isHost === "True") { alert("Error: " + msg_content['error']); }
		} else if (msg_type === 'add_song'){
            let rows =  '';
            var id = msg_content['id'];
            var name = msg_content['name'];
            var url =  msg_content['url'];
            var description =  msg_content['description'];
            if(isHost === "True"){
                            rows += `
        <tr>
            <td>
            <div class = "to_right" onclick=playMusic(this.id) id="${url}" value="${url}" > </div>
            </td>
            <td>${name}</td>
            <td>${description}</td>
            <td>
                <button class="btn deleteBtn btn-dark" name="remove_song" value="${id}">Remove</button>
            </td>
            <td>
                <button class="btn btn-dark" name="song" value="${id}" data-id="${id}" onclick=likeSongs(this) >Like</button>
            </td>
        </tr>`;
            }else{
            rows += `
        <tr>
            <td>${name}</td>
            <td>${description}</td>
            <td>
                <button class="btn btn-dark" name="song" value="${id}" data-id="${id}" onclick=likeSongs(this) >Like</button>
            </td>
        </tr>`;
            }

        $('#myTable > tbody').append(rows);

        if(isHost === "True"){
            //bind remove song handlers again when a new song being added
            $("[name='remove_song']").bind("click", function(){
                console.log('delete song js triggered!');
                var musicId  =  $(this)["0"].value;
                var data = {'id': musicId};
                console.log("remove songs sent!")
                webSocket.send(JSON.stringify({
                    'msg_type': 'remove_song',
                    'msg_content': data,
                }));
                $(this).parents()[1].remove();
            })
            }
        }

        //remove songs
        if (msg_type === 'remove_song' && !('error' in msg_content ) ){
            var id = msg_content['id'];
            var isHost = $("#music-bar").attr("data-isHost")
            if(isHost === "False"){            // host song has already been removed
                var button = $('button' + '[value = "'+ id+'"]')["0"];
                console.log(button);
                var row = button.parentElement.parentElement;
                row.remove();
            }
        }
    }
}

//get http response
function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;
}
