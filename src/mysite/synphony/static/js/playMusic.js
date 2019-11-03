function playMusic(val) {
    var audio = document.getElementById('music-bar');
    var audio_source = document.getElementById('audiosrc');
    // console.log(val);
     console.log(audio_source);
     console.log(audio);
    audio_source.src = val.toString();
    audio.load();//PAY ATTENTION!
    audio.play();
  }
