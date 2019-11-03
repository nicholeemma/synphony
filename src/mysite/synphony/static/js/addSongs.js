// csrf token
var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function addSongs(val) {
    console.log('add songs js triggered!')
    console.log("this is the song id" + val)
    // get music file url
    var url = "https://api.imjad.cn/cloudmusic/?type=song&id=" + val
    var json_obj = JSON.parse(Get(url));
    var musicUrl = json_obj["data"][0]["url"];

    //get song info
        //["Hello", " by: 王霏霏（Fei）/ 王嘉尔  Add"]
        // 0: "Hello"
        // 1: " by: 王霏霏（Fei）/ 王嘉尔  Add"
    var object = document.getElementById(val);
    var song_info = object.parentElement.textContent;
    var name = song_info.split(',')[0];
    var description = song_info.split(',')[1].slice(0, -5);
    var data = {};
    data[name] = name;
    data[description] = description;
    data[url] = musicUrl;
    console.log("data to be sent to server: " + data)
    // //create a new source for media type and append to audio
    // var source = document.createElement("SOURCE");
    // source.id = val;
    // source.src = musicUrl;
    // source.type = "audio/mpeg";
    // var audio = document.getElementById("music-bar")
    // audio.appendChild(source)

    $.ajax({
        url:  '/synphony/adgjlsfhk/addSongs',
        type:  'post',
        dataType:  'json',
        data: data,
        success: function  (data) {
        let rows =  '';
        console.log("response: " + data);
        data.forEach(music => {
        rows += `
        <tr>
            <td>${music.name}</td>
            <td>${music.description}</td>
            <td>
                <button class="btn deleteBtn" data-id="${music.id}">Delete</button>
                <button class="btn updateBtn" data-id="${music.id}">Update</button>
            </td>
        </tr>`;
    });
    $('#myTable > tbody').append(rows);
        // $(el).parents()[1].remove()s
        }
    });
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
