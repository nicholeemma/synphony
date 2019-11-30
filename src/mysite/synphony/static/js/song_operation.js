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

// function addSongs(val) {
//     console.log('add songs js triggered!')
//     console.log("this is the song id" + val)
//     // get music file url
//     var url = "https://api.imjad.cn/cloudmusic/?type=song&id=" + val
//     var json_obj = JSON.parse(Get(url));
//     var musicUrl = json_obj["data"][0]["url"];

//     //get song info
//         //["Hello", " by: 王霏霏（Fei）/ 王嘉尔  Add"]
//         // 0: "Hello"
//         // 1: " by: 王霏霏（Fei）/ 王嘉尔  Add"
//     var object = document.getElementById(val);
//     var song_info = object.textContent;
//     var name = song_info.split(',')[0];
//     var description = song_info.split(',')[1];
//     var data = {};
//     data['name'] = name;
//     data['description'] = description;
//     data['url'] = musicUrl;
//     console.log("data to be sent to server: " + data)

//     $.ajax({
//         url:  location.pathname.split("/")[2] + '/addSongs',
//         type:  'post',
//         dataType:  'json',
//         data: data,
//         success: function (response) {
//         //TODO if response only contains error -> display song cannot be added!
//         let rows =  '';
// //       Object.keys(response).forEach(function (key){
//         var id = response.music['id'];
// //Sample response :
// // {'music':
// //     {'id': 32,
// //     'name': 'Love Story',
// //     'url': 'https://m7.music.126.net/20191103112226/77adcb0833b2b86b6c02ab4bca779c53/ymusic/850b/d83b/93b2/bdecc59eb55cd9dd81ff024f987cf98e.mp3',
// //     'description': 'by: Various Artists',
// //     'lyrics': '',
// //     'liked_user': []}}
//         rows += `
//         <tr>
//             <td>
//             <div class = "to_right" onclick=playMusic(this.id) id="${musicUrl}" value="${musicUrl}" > </div>
//             </td>
//             <td>${name}</td>
//             <td>${description}</td>
//             <td>
//                 <button class="btn deleteBtn btn-dark" data-id="${id}">Remove</button>
//             </td>
// 			<td>
// 				<button class="btn btn-dark" data-id="${id}" onclick=likeSongs(this) >Like</button>
// 			</td>
//         </tr>`;
//  //   });
//     $('#myTable > tbody').append(rows);
//     $('.deleteBtn').each((i, elm) => {
//         $(elm).on("click",  (e) => {
//             deleteSongs ($(elm))
//         })
//     }
//     )}
//     });
// }

// function Get(yourUrl){
//     var Httpreq = new XMLHttpRequest(); // a new request
//     Httpreq.open("GET",yourUrl,false);
//     Httpreq.send(null);
//     return Httpreq.responseText;
// }


// function  deleteSongs(el){
//     console.log('delete song js triggered!');
//     musicId  =  $(el).data('id')
//     data = {'id': musicId};
//     console.log('music id: ' + musicId);
//     $.ajax({
//         url:  location.pathname.split("/")[2] + '/deleteSongs',
//         type:  'post',
//         dataType:  'json',
//         data: data,
//         success:  function (data) {
//             $(el).parents()[1].remove()
//         }
//     });
// }
function  likeSongs(el){
    console.log('like song js triggered!');
    musicId  =  $(el).data('id')
    data = {'id': musicId};
    console.log('music id: ' + musicId);
    $.ajax({
        url:  location.pathname.split("/")[2] + '/likeSongs',
        type:  'post',
        dataType:  'json',
        data: data,
        success:  function (response) {
			var textBtn = 'Like'
            if($(el).html() === 'Like' && !(response.hasOwnProperty('error'))) {
				textBtn = 'Unlike'
			}
			$(el).html(textBtn)
        }
    });
}

//existing music urls on page
let musicList = document.getElementsByClassName("to_right");
//list of music urls
let musicurllist = [];

function addMusicToList_loop(){
    musicurllist = [];
    for (url of musicList) {//TODO BACKWARDS!
    musicurllist.push(url.getAttribute("value"));}
}

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1)); // random index from 0 to i

    // swap elements array[i] and array[j]
    // we use "destructuring assignment" syntax to achieve that
    // you'll find more details about that syntax in later chapters
    // same can be written as:
    // let t = array[i]; array[i] = array[j]; array[j] = t
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}


function play_all(context){
    //initialize music url list
    addMusicToList_loop();
    //shuffle if needed
    if(context === 'shuffle'){
         musicurllist = shuffle(musicurllist);
     }
    var audio = document.getElementById('music-bar');

    //get last element from music url list
    var src = musicurllist.pop();
    audio.src = src;
    //shift the pop element to the front (s.t. loop)
    musicurllist.unshift(src);
    //when the current song stops playing, call playEndedHandler (change song)
    audio.addEventListener("ended",playEndedHandler,false);
    //play the current song
    audio.load();
    audio.play();
    // must set to false, otherwise would be single-song loop
    audio.loop = false;
    function playEndedHandler(){
        src = musicurllist.pop();
        audio.src = src;
        musicurllist.unshift(src);
        audio.load();
        audio.play();
    }
}

//fetch resource url
function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;
}

//play a song when triangle button clicked
function playMusic(val) {
    var audio = document.getElementById('music-bar');
    // var audio_source = document.getElementById('audiosrc');
    // console.log(val);
    console.log(audio);
    audio.src = val.toString();
    audio.load();//PAY ATTENTION!
    audio.play();
  }
