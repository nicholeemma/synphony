from django.shortcuts import render
import requests


def index(request):
    if request.method == 'POST' and 'song-name-submit' in request.POST:
        return displaySongList(request)
    return render(request, 'synphony/index.html', {'list': []})


def displaySongList(request):
    title = request.POST.get('song-name')

    # TODO currently, only search songs by title
    # search songs using third-party API of Netease Music
    # use song title to call api
    URL = "https://api.imjad.cn/cloudmusic/?type=search&search_type=1&s=" + title
    r = requests.get(url=URL)
    data = r.json()
    # if not found -> API will return the following
    #{"result":{"songCount":0},"code":200}

    # process json -> dic list of Songs to be displayed to client
    # i.e. name, id, author
    list = []
    for i in data['result']['songs']:
        dic = {}
        dic['name'] = i['name']
        dic['id'] = i['id']
        dic['ar'] = ""
        for j in i['ar']:
            dic['ar'] += j['name'] + "/ "
        dic['ar'] = dic['ar'][0: -2];# remove last "/ "
        list.append(dic)
    return render(request, 'synphony/index.html', {'list': list})
