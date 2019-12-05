
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Music(models.Model):

    name = models.CharField(max_length=30)
    url = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    lyrics = models.TextField(max_length=255, blank=True)
    liked_user = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Studio(models.Model):

    name = models.CharField(max_length=30)
    music = models.ManyToManyField(Music)
    # record whether the studio is active or not
    status = models.BooleanField(default=True)
    # constraint will be set in form.py cannot be larger than 10
    headcount = models.IntegerField(default=10)
    # field_for_sharablelink
    link = models.CharField(max_length=16)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now() - timedelta(hours=5))
    end_time = models.DateTimeField(default=datetime.now() - timedelta(hours=3))
    # end_time is not used for now. In P2 , when VIP users customize studio lifetime, it will come into use.
    # Right now, lifetime for each studio is defaulted to 2 hours.


class Participant(models.Model):

    participant_user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=11, default='participant')
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)


class Comment(models.Model):

    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    commented_on = models.ForeignKey(Studio, on_delete=models.CASCADE)

# This model is not used for now.
class History(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
