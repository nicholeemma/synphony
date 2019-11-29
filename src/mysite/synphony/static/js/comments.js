

   var key = {{ key_json }}; //studio hashed key
   // open new sockect
    var chatSocket = new WebSocket('ws://' + window.location.host + '/ws' + window.location.pathname);
    // var chatSocket = new WebSocket(
    //     'ws://' + window.location.host +
    //     '/ws/synphony/' + key + '/');

    // append comment history
    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        console.log("message received: " + message)
        document.querySelector('#commentcontent').innerHTML += (message + '\n');
    };

    //disonnect
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    // post comment
    document.querySelector('#commentinput').focus();
    document.querySelector('#commentinput').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#postComment').click();
        }
    };

    document.querySelector('#postComment').onclick = function(e) {
        var messageInputDom = document.querySelector('#commentinput');
        var message = messageInputDom.value;
        var user = "{{user.username}}: ";
        console.log(user)
        chatSocket.send(JSON.stringify({
            'message': user + message
        }));

        console.log(message + " sent!")
        messageInputDom.value = '';
    };
