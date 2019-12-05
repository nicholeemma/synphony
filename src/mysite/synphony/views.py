
from django.shortcuts import render
import requests
import hashlib
import random
import json
import sys
from django.shortcuts import redirect
# from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Studio, Music, Participant, Comment, History
from .forms import MusicForm, CreateStudioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
import sys
import datetime
from datetime import timedelta
from django.contrib import messages

# sys.stdout.reconfigure(encoding='utf-8')


@login_required
def index(request, key=""):

    ctx = dict()
    try:
        cur_studio = Studio.objects.get(link__exact=key)
        ctx['isHost'] = (cur_studio.host.id == request.user.id)
        ctx['isActive'] = (cur_studio.status is True)
        # print(ctx['isHost'])
        # print(ctx['isActive'])
    except:
        print("Studio does not exist!")
        return redirect(reverse('home'))

    music_list, music_list_des = [], []
    music_url_list = []
    for s_music in cur_studio.music.all():
        music_list.append(s_music.id)
        music_url_list.append(s_music.url)
        music_list_des.append(s_music.description)
    musics = Music.objects.filter(id__in=music_list)

    list = []
    if request.method == 'POST' and 'song-name-submit' in request.POST:
        list = displaySongList(request)

    cur_studio = Studio.objects.get(link__exact=key)
    startTime = Studio.objects.filter(link=key).values('start_time')
    endTime = Studio.objects.filter(link=key).values('end_time')
    timea = ''
    timeb = ''
    for s in startTime:
        timea = s['start_time']
    for e in endTime:
        timeb = e['end_time']
        format = "%b %d %Y %H:%M:%S"
        st = datetime.datetime.strftime(timea, format)
        en = datetime.datetime.strftime(timeb, format)
    # comments = Comment.objects.all()
    ctx.update({"musics": musics, "list": list, "user": request.user,
                'key_json': mark_safe(json.dumps(key)), "studio": cur_studio, "startTime": mark_safe(json.dumps(st)), "endTime": mark_safe(json.dumps(en))})
    # check / add new user as participants of this studio
    addParticipants(ctx['user'], cur_studio)
    return render(request, 'synphony/index.html', ctx)


def addParticipants(user, studio):
    user_list = Participant.objects.filter(studio=studio)
    if user not in user_list:
        participant = Participant(participant_user=user, studio=studio)
        participant.save()


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
    errors = {}
    if request.method == 'POST':
        try:
            login(request, user)
            return render(request, 'synphony/homepage.html')
        except:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            form = UserCreationForm()
            context = {
                'form': form,
                'errors': 'Invalid login credentials, please try again!'
            }
            return render(request, 'synphony/login.html', context)
    else:
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        else:
            form = UserCreationForm()
            context = {'form': form}
            return render(request, 'synphony/login.html', context)


def home_page(request):
    # if('synphony' not in request.path):
    #   return redirect('/synphony')
    if request.user.is_authenticated:
        return render(request, 'synphony/homepage.html')
    else:
        return redirect(reverse('login'))


def user_logout(request):
    logout(request)
    return render(request, 'synphony/logout.html')


@login_required
def studio_view(request):
    error = ""
    studios = Studio.objects.filter(host=request.user, status=True)
    hasStudio = (len(studios) >= 1)
    if request.method == 'POST':
        # Check exisiting studio

        if "jumpstudio" in request.POST:
            # link = request.POST["activestudio"]
            link = request.POST.get('jumpstudio')
            print(link)
            return redirect(reverse('index', args=[link]))
        if "createstudio" in request.POST and len(studios) >= 1:
            form = CreateStudioForm()
            error = "You can only one active studio, go to history find your active studio"
            print("you can only have one")
        else:
            form = CreateStudioForm(request.POST)
            if form.is_valid():
                hashcode = (str(form.cleaned_data) +
                            str(random.random())).encode('utf-8')
                link = hashlib.md5(hashcode).hexdigest()[:16]
                newStudio = Studio(
                    name=form.cleaned_data['name'],
                    link=link,
                    host=request.user
                )
                # startTime = Studio.objects.get(start_time=studios)
                newStudio.save()
                return redirect(reverse('index', args=[link]))
    else:
        form = CreateStudioForm()

    context = {'form': form, 'error': error,
               'studios': studios, 'hasStudio': hasStudio}
    return render(request, 'synphony/create_studio.html', context)


@login_required
def view_history(request):
    comments = Comment.objects.filter(user_name=request.user)
    studios = Studio.objects.filter(host=request.user)
    participated_records = Participant.objects.filter(participant_user=request.user)
    print(studios)
    musics = request.user.music_set.all()
    hasStudio = (len(studios) >= 1)
    hasParticipation = (len(participated_records) >= 1)
    hasComment = (len(comments) >= 1)
    hasMusic = (len(musics) >= 1)
    if request.method == "POST":
        if "jumpstudio" in request.POST:
            link = request.POST.get('jumpstudio')
            print(link)
            return redirect(reverse('index', args=[link]))
    context = {"comments": comments, "studios": studios, "participated_records": participated_records, "musics": musics, "hasStudio": hasStudio, "hasParticipation": hasParticipation, "hasComment": hasComment, "hasMusic": hasMusic}
    return render(request, "synphony/view_history.html", context)


def displaySongList(request):
    print(request.path)

    title = request.POST.get('song-name')
    # only search songs by title
    # search songs using third-party API of Netease Music
    # use song title to call api

    URL = "https://netmusicapi.herokuapp.com/search?keywords=" + title
    # URL = "http://localhost:3000/search?keywords=" + title

    r = requests.get(url=URL)
    print(r.encoding)
    print(r.headers['content-type'])

    print(r)
    data = r.json()
    # data
    # data = sdata, "utf-8", errors="ignore")

    print(data)
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
        for j in i['artists']:
            dic['ar'] += j['name'] + "/ "
        dic['ar'] = dic['ar'][0: -2]  # remove last "/ "
        list.append(dic)

    return list


# commented out -> has migrated to websockets
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


def closeStudio(request, key=""):

    rsp = dict()

    # check login status
    if not request.user.is_authenticated:
        rsp['error'] = "Please login to close studio!"
        return JsonResponse(rsp)

    # check if studio exists
    try:
        cur_studio = Studio.objects.get(link__exact=key)
        if not cur_studio.status:
            rsp['error'] = "Studio already closed!"
            return JsonResponse(rsp)
        cur_studio.status = False
        cur_studio.save()
    except:
        rsp['error'] = "Studio not found!"
        return JsonResponse(rsp)

    return JsonResponse(rsp)
