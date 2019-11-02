$(function () {
    console.log("playlist.js loaded!");
});

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


$.ajax({
    // TODO need to incorporate suqi's url
    url:  '/studio/playList',
    type:  'get',
    dataType:  'json',
    success: function  (data) {
        let rows =  '';
        data.rooms.forEach(room => {
        rows += `
        <tr>
            <td>${room.room_number}</td>
            <td>${room.name}</td>
            <td>${room.nobeds}</td>
            <td>${room.room_type}</td>
            <td>
                <button class="btn deleteBtn" data-id="${room.id}">Delete</button>
                <button class="btn updateBtn" data-id="${room.id}">Update</button>
            </td>
        </tr>`;
    });
    $('#myTable > tbody').append(rows);
    $('.deleteBtn').each((i, elm) => {
        $(elm).on("click",  (e) => {
            deleteRoom($(elm))
        })
    })
    }
});


function  deleteRoom(el){
    roomId  =  $(el).data('id')
    $.ajax({
        url:  `/rooms/delete/${roomId}`,
        type:  'post',
        dataType:  'json',
        success:  function (data) {
            $(el).parents()[1].remove()
        }
    });
}
