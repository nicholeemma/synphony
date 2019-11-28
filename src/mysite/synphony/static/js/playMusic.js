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

//   window.onload = function(){
//     //存放音乐列表，根据音乐文件路径，进行填写
//     var musicList = ["/skins/skin/bj/audio/1.mp3","/skins/skin/bj/audio/1.mp3"]
//     playMusic(musicList);
// }
 
function play_all(musicList){
  // location.reload()
  var musicList=document.getElementsByClassName("musicurl")
  var musicurllist = []
  for (url of musicList) {
    musicurllist.push(url.innerHTML)
  }
  console.log(musicurllist)
    var myAudio = document.getElementById('music-bar');
    // //是否进行预加载
    // myAudio.preload = false;
    // //是否显示隐藏按钮
    // myAudio.controls = true;
    // myAudio.hidden = true;
    //从音乐列表中，获取最后一个音乐（并删除）
    var src = musicurllist.pop();
    myAudio.src =src;
    //将最后一个音乐添加到数组的开头，这样实现循环
    musicurllist.unshift(src);
    //绑定音乐结束事件，当音乐播放完成后，将会触发playEndedHandler方法
    myAudio.addEventListener("ended",playEndedHandler,false);
    //播放当前音乐
    myAudio.play();
    document.getElementById("musicaudio").appendChild(myAudio);
    //将循环播放关闭，如果开启，将不能触发playEndedHandler方法，只能进行单曲循环
    myAudio.loop = false;
 
    function playEndedHandler(){
        src = musicurllist.pop();
        myAudio.src = src;
        musicurllist.unshift(src);
        myAudio.play();
    }
}
