from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Playlist(models.Model):
	title = models.CharField(max_length = 50, unique = True)
	music = models.ManyToManyField(Music)
	description = models.TextField()
	image = models.FileField(upload_to = "")
	owner = models.ForeignKey(MUser, on_delete = models.CASCADE)


class MUser(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	collections = models.ManyToManyField(Playlist)
	likes = models.ManyToManyField(Playlist)


class Music(models.Model):
	url = models.URLField()
	title = models.CharField(max_length = 50, unique = True)
	description = models.TextField()
	image = models.FileField(upload_to = "")


class Studio(models.Model):
	host = models.ForeignKey(MUser, on_delete = models.CASCADE)
	participants = models.ManyToManyField(MUser, on_delete = models.CASCADE)
	playlist = models.ForeignKey(Playlist)
	date = models.DateField(auto_now_add = True)

class Comment(models.Model):
	studio = models.ForeignKey(MUser, on_delete = models.CASCADE)
	user = models.ForeignKey(MUser, on_delete = models.CASCADE)
	date = models.DateField(auto_now_add = True)
	