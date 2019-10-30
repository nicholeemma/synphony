
function addSongs(val) {
    console.log("this is the song id" + val)
    var url = "https://api.imjad.cn/cloudmusic/?type=song&id=" + val
    var json_obj = JSON.parse(Get(url));
    var musicUrl = json_obj["data"][0]["url"];
    //console.log("this is json response: "+ musicUrl);
    var source = document.createElement("SOURCE");
    source.id = val;
    source.src = musicUrl;
    source.type = "audio/mpeg";
    var audio = document.getElementById("music-bar")
    audio.appendChild(source)

    // var text = document.getElementById("").value;
    // li.appendChild(document.createTextNode(text));
    // document.getElementById("todolist").appendChild(li);
}

function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;
}



// function buttonClickFunction() {
//     document.getElementById("addBtn").addEventListener("click");
//     var li = document.createElement("li");
//     var text = document.getElementById("textfield").value;
//     li.appendChild(document.createTextNode(text));
//     document.getElementById("todolist").appendChild(li);
// }
