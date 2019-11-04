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
import hashlib, random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def index(request, key=""):

	try:
		cur_studio = Studio.objects.get(link__exact = key)
	except:
		print("Studio does not exist!")
		return redirect(reverse('index',args = ["0123456789abcdef"]))
	
	music_list, music_list_des = [], []
	for s_music in cur_studio.music.all():
		music_list.append(s_music.id)
		music_list_des.append(s_music.description)
	musics = Music.objects.filter(id__in=music_list)

	list = []
	if request.method == 'POST' and 'song-name-submit' in request.POST:
		list = displaySongList(request)

	ctx = {"musics": musics, "list": list, "user": request.user}
	return render(request, 'synphony/index.html', ctx)


# def signup(request):
# 	if request.method == 'POST':
# 		form = UserCreationForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = request.POST.get('username')
# 			password = request.POST.get('password')
# 			user = authenticate(username=username, password=password)
# 			login(request, user)
# 			return redirect('index')
# 	else:
# 		form = UserCreationForm()
# 	context = {'form': form}
# 	return render(request, 'synphony/signup.html', context)


def signup(request):
	if request.user.is_authenticated:
		url = 'http://127.0.0.1:8000/synphony/0123456789abcdef'
		return redirect(url)
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = request.POST.get('username')
			password = request.POST.get('password1')
			user = authenticate(username=username, password=password)
			print(user)
			login(request, user)
			url = 'http://127.0.0.1:8000/synphony/0123456789abcdef'
			return redirect(url)
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
			hashcode = (str(form.cleaned_data) + str(random.random())).encode('utf-8')
			link = hashlib.md5(hashcode).hexdigest()[:16]
			newStudio = Studio(
					name = form.cleaned_data['name'],  
					status = form.cleaned_data['status'], 
					link = link, 
					host = form.cleaned_data['host']
				)
			newStudio.save()
			newStudio.music.add(*(list(form.cleaned_data['music'])))
			return redirect(reverse('index',args = [link]))
	else:
		form = CreateStudioForm()
	context = {'form': form}
	return render(request, 'synphony/create_studio.html', context) 


def displaySongList(request):
<<<<<<< HEAD
    print(request.path)

# # Commented out since search API unusable
#     title = request.POST.get('song-name')
#     # TODO currently, only search songs by title
#     # search songs using third-party API of Netease Music
#     # use song title to call api
#     URL = "https://api.imjad.cn/cloudmusic/?type=search&search_type=100&s=" + title
#     r = requests.get(url=URL)
#     data = r.json()
#     print(data)
#     # if not found -> API will return the following
#     #{"result":{"songCount":0},"code":200}

#     # process json -> dic list of Songs to be displayed to client
#     # i.e. name, id, author
#     list = []
#     for i in data['result']['songs']:
#         dic = {}
#         dic['name'] = i['name']
#         dic['id'] = i['id']
#         dic['ar'] = ""
#         for j in i['ar']:
#             dic['ar'] += j['name'] + "/ "
#         dic['ar'] = dic['ar'][0: -2];  # remove last "/ "
#         list.append(dic)
    list = []
    dic_1 = {}
    dic_1['name'] = '近く远い斜め色の空'
    dic_1['ar'] = 'DDBY'
    dic_1['id'] = '715681'
    list.append(dic_1)
    dic_2 = {}
    dic_2['name'] = '淡々泡々'
    dic_2['ar'] = 'Foxtail-Grass Studio'
    dic_2['id'] = '27669786'
    list.append(dic_2)
    dic_3 = {}
    dic_3['name'] = 'ティコ'
    dic_3['ar'] = '押尾コータロー'
    dic_3['id'] = '22822613'
    list.append(dic_3)
    dic_4 = {}
    dic_4['name'] = '信仰は存活の為に~Give Me Full of Your Tears'
    dic_4['ar'] = '九条咲夜'
    dic_4['id'] = '252479'
    list.append(dic_4)
    return list

# display the playlist for an active studio
=======
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
>>>>>>> a00d036c9995ef771fa588cf60f7173930701d07


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
		music.liked_user.get(id = request.user.id)
		music.liked_user.remove(request.user)
	except:
		# Like music
		music.liked_user.add(request.user)

	return JsonResponse(rsp)