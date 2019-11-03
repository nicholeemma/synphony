from django.shortcuts import render
import requests
from django.shortcuts import redirect
# from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Studio, Music, Syner, Like, Participant, Comment, History
from .forms import MusicForm


def getRoomHashLink(path):
    path_list = path.split('/')
    token_index = path_list.index('synphony') + 1
    token = str(path_list[token_index])
    return token


def index(request):
    # content = {}
    # content["show"] = ""
    path = request.path
    token = getRoomHashLink(path)
    print(token)
    # TODO: redirect user to some page if studio does not exist
    cur_studio = Studio.objects.get(link=token)
    music_list = []
    music_list_des = []
    for s_music in cur_studio.music.all():
        music_list.append(s_music.id)
        music_list_des.append(s_music.description)
    musics = Music.objects.all().filter(id__in=music_list)
    list = []
    if request.method == 'POST' and 'song-name-submit' in request.POST:
        list = displaySongList(request)
    return render(request, 'synphony/index.html', {"musics": musics, "list": list})
    # ,"show":error_message


def displaySongList(request):
    print(request.path)
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
        dic['ar'] = dic['ar'][0: -2];  # remove last "/ "
        list.append(dic)
    return list

# display the playlist for an active studio


def showStudio(request):
    pass

# add a song to the playlist for an active studio


def addSongsToStudio(request):
    print(request.POST)
    music_form = MusicForm(request.POST)
    rsp = dict()
    if(music_form.is_valid()):
        music = music_form.save()
        # get studio hashed token
        token = request.path.split('/')[-2]  # path = synphony/adgjlsfhk/addSongs
        studio = Studio.objects.get(link=token)
        studio.music.add(music)
        rsp['music'] = model_to_dict(music)
        print(rsp)
    else:
        rsp['error'] = "form not valid!"
        print("forms not valid!")
    return JsonResponse(rsp)


# remove a song from the playlist for an active studio


def deleteSongsFromPlayList(request):
    music_id = request.POST.get('id')
    # check if music_id has corresponding music
    music_set = Music.objects.filter(pk=music_id)
    if music_set.count() > 0:
        music = Music.objects.get(pk=music_id)
        # get current studio
        path = request.path
        token = getRoomHashLink(path)
        cur_studio = Studio.objects.get(link=token)
        # check if music in cur_studio
        if cur_studio.music.filter(pk=music_id).count() > 0:
            cur_studio.music.remove(music)
    rsp = dict()
    return JsonResponse(rsp)
