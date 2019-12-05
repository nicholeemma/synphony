// song operation: add , remove, like, etc.

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
