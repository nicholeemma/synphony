
from django.shortcuts import render
import requests
from django.shortcuts import redirect
# from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Studio, Music, Participant, Comment, History
from .forms import MusicForm, CreateStudioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import hashlib
import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
import json
import sys

# sys.stdout.reconfigure(encoding='utf-8')
def index(request, key=""):

    try:
        cur_studio = Studio.objects.get(link__exact=key)
    except:
        print("Studio does not exist!")
        return redirect(reverse('index', args=["0123456789abcdef"]))

    music_list, music_list_des = [], []
    for s_music in cur_studio.music.all():
        music_list.append(s_music.id)
        music_list_des.append(s_music.description)
    musics = Music.objects.filter(id__in=music_list)

    list = []
    if request.method == 'POST' and 'song-name-submit' in request.POST:
        list = displaySongList(request)

    comments = Comment.objects.all()
    participants = Participant.objects.filter(studio=cur_studio)
    ctx = {"musics": musics, "list": list, "user": request.user,
           'key_json': mark_safe(json.dumps(key)), "comments": comments, "participants": participants}
    return render(request, 'synphony/index.html', ctx)


# def signup(request):
#   if request.method == 'POST':
#       form = UserCreationForm(request.POST)
#       if form.is_valid():
#           form.save()
#           username = request.POST.get('username')
#           password = request.POST.get('password')
#           user = authenticate(username=username, password=password)
#           login(request, user)
#           return redirect('index')
#   else:
#       form = UserCreationForm()
#   context = {'form': form}
#   return render(request, 'synphony/signup.html', context)


def signup(request):
    if request.user.is_authenticated:
        return render(request, 'synphony/homepage.html')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(username=username, password=password)
            print(user)
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'synphony/signup.html', context)


def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password1')
    user = authenticate(request, username=username, password=password)
    if request.method == 'POST':
        try:
            login(request, user)
            return render(request, 'synphony/homepage.html')
        except:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        else:
            form = UserCreationForm()
            context = {'form': form}
            return render(request, 'synphony/login.html', context)


def home_page(request):
    if request.user.is_authenticated:
        return render(request, 'synphony/homepage.html')
    else:
        return render(request, 'synphony/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'synphony/logout.html')


@login_required
def studio_view(request):
    if request.method == 'POST':
        form = CreateStudioForm(request.POST)
        if form.is_valid():
            hashcode = (str(form.cleaned_data) + str(random.random())).encode('utf-8')
            link = hashlib.md5(hashcode).hexdigest()[:16]
            newStudio = Studio(
                name=form.cleaned_data['name'],
                link=link,
                host=request.user
            )
            newStudio.save()
            # newStudio.music.add(*(list(form.cleaned_data['music'])))
            return redirect(reverse('index', args=[link]))
    else:
        form = CreateStudioForm()
    context = {'form': form}
    return render(request, 'synphony/create_studio.html', context)
def view_history(request):
    comments = Comment.objects.filter(user_name=request.user) 
    
    studios = Studio.objects.filter(host=request.user)
    musics = request.user.music_set.all()
    return render(request,"synphony/view_history.html",{"comments":comments,"studios":studios,"musics":musics}) 

def displaySongList(request):
    print(request.path)

# Commented out since search API unusable
    title = request.POST.get('song-name')
    # TODO currently, only search songs by title
    # search songs using third-party API of Netease Music
    # use song title to call api
    URL = "http://localhost:3000/search?keywords=" + title
    r = requests.get(url=URL)
    print(r.encoding)
    print(r.headers['content-type'])

    print(r)
    data = r.json()
    # data
    # data = sdata, "utf-8", errors="ignore")

    print(data)
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
        for j in i['artists']:
            dic['ar'] += j['name'] + "/ "
        dic['ar'] = dic['ar'][0: -2]  # remove last "/ "
        list.append(dic)
    # list = []
    # dic_1 = {}
    # dic_1['name'] = '近く远い斜め色の空'
    # dic_1['ar'] = 'DDBY'
    # dic_1['id'] = '715681'
    # list.append(dic_1)
    # dic_2 = {}
    # dic_2['name'] = '淡々泡々'
    # dic_2['ar'] = 'Foxtail-Grass Studio'
    # dic_2['id'] = '27669786'
    # list.append(dic_2)
    # dic_3 = {}
    # dic_3['name'] = 'ティコ'
    # dic_3['ar'] = '押尾コータロー'
    # dic_3['id'] = '22822613'
    # list.append(dic_3)
    # dic_4 = {}
    # dic_4['name'] = '信仰は存活の為に~Give Me Full of Your Tears'
    # dic_4['ar'] = '九条咲夜'
    # dic_4['id'] = '252479'
    # list.append(dic_4)
    return list


# display the playlist for an active studio
def showStudio(request):
    pass

# add a song to the playlist for an active studio


def addSongsToStudio(request, key=""):
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
