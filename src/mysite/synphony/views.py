from django.shortcuts import render
import requests
from django.shortcuts import redirect
# from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Studio, Music, Syner, Participant, Comment, History
from .forms import MusicForm, CreateStudioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse

def index(request, key=""):
        # content = {}
        # content["show"] = ""
    music_list = []
    music_list_des = []
    try:
        cur_studio = Studio.objects.get(link__exact=key)
    except:
        # TODO: redirect user to some page if studio does not exist
        print("Studio does not exist!")
        return render(request, 'synphony/index.html')
    for s_music in cur_studio.music.all():
        music_list.append(s_music.id)
        music_list_des.append(s_music.description)
    musics = Music.objects.all().filter(id__in=music_list)
    list = []
    if request.method == 'POST' and 'song-name-submit' in request.POST:
        list = displaySongList(request)
    ctx = {"musics": musics, "list": list, "user": request.user}
    return render(request, 'synphony/index.html', ctx)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'synphony/signup.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        try:
            user = authenticate(request, username=username, password=password)
            login(request,user)
            url = 'http://127.0.0.1:8000/synphony/0123456789abcdef'
            return redirect(url)
        except:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'synphony/login.html', context)


def user_logout(request):
    logout(request)
    return render(request, 'synphony/logout.html')


@login_required
def studio_view(request):
    if request.method == 'POST':
        form = CreateStudioForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'synphony/create_studio.html', context)
    else:
        form = CreateStudioForm()
    context = {'form': form}
    return render(request, 'synphony/create_studio.html', context)


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
    # {"result":{"songCount":0},"code":200}

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
        dic['ar'] = dic['ar'][0: -2]  # remove last "/ "
        list.append(dic)
    return list


# display the playlist for an active studio
def showStudio(request):
    pass

# add a song to the playlist for an active studio


def addSongsToStudio(request, key = ""):
    # print(request.POST)
    rsp = dict()

    try:
        studio = Studio.objects.get(link__exact=key)
    except:
        rsp['error'] = "Studio not found!"
        return JsonResponse(rsp)

    music_form = MusicForm(request.POST)
    if(music_form.is_valid()):
        music = music_form.save()
        studio.music.add(music)
        rsp['music'] = model_to_dict(music)
        print(rsp)
    else:
        rsp['error'] = "form not valid!"
        print("forms not valid!")
    return JsonResponse(rsp)


# remove a song from the playlist for an active studio
def deleteSongsFromPlayList(request, key=""):

    rsp = dict()
    try:
        cur_studio = Studio.objects.get(link__exact=key)
    except:
        rsp['error'] = "Studio not found!"
        return JsonResponse(rsp)

    music_id = request.POST.get('id')
    # check if music_id has corresponding music
    music_set = Music.objects.filter(pk=music_id)
    if music_set.count() > 0:
        music = Music.objects.get(pk=music_id)
        # check if music in cur_studio
        if cur_studio.music.filter(pk=music_id).count() > 0:
            cur_studio.music.remove(music)

    return JsonResponse(rsp)


# like a song from the playlist for an active studio
def likeSongsFromPlayList(request, key=""):

    rsp = dict()

    # check login status
    if not request.user.is_authenticated:
        rsp['error'] = "Please login to like music!"
        return JsonResponse(rsp)

    # check if studio exists
    try:
        cur_studio = Studio.objects.get(link__exact=key)
    except:
        rsp['error'] = "Studio not found!"
        return JsonResponse(rsp)

    # check if music in cur_studio
    try:
        music_id = request.POST.get('id')
        music = cur_studio.music.get(pk=music_id)
    except:
        rsp['error'] = "Music not found in current studio!"
        return JsonResponse(rsp)

    try:
        # Unlike music
        music.liked_user.get(id=request.user.id)
        music.liked_user.remove(request.user)
    except:
        # Like music
        music.liked_user.add(request.user)

    return JsonResponse(rsp)