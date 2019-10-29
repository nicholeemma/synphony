from django.shortcuts import render


def index(request):
    if request.method == 'POST' and 'song-name-submit' in request.POST:
        return displaySongList(request)
    return render(request, 'synphony/index.html', {})


def displaySongList(request):
    title = request.POST.get('get-list')
    # use song title to call api
    # get json
    # process json -> dic listof Songs
    # id, name, author - list
    # render page with var list
    pass
