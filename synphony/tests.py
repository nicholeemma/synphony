from django.test import TestCase

# Create your tests here.
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
import time
# from selenium import webdriver
from django.test import Client
# from selenium.webdriver.support.ui import Select
from django.test.utils import override_settings
from django.contrib.contenttypes.models import ContentType

import os

class SynphonyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')
        music = Music.objects.create(name="hello", url="http://www.hello.com", 
            description="Good music", lyrics="hello")
        music.liked_user.add(self.user)
        music.save()
        studio = Studio.objects.create(name="teststudio", status=True, headcount =10, 
            link="asdkjfklds", host=self.user)
        studio.music.add(music)
        studio.save()
        p = Participant.objects.create(participant_user=self.user,studio=studio)
        p.save()
        comment = Comment.objects.create(user_name = self.user,text="testcomment", commented_on=studio)
        comment.save()
        history = History.objects.create(user = self.user, studio= studio)
        history.save()

    def test_user(self):
        """Animals that can speak are correctly identified"""
        
        self.assertEqual(self.user.username, 'jacob')
    def test_music(self):
        t_music = Music(name="hello")
        self.assertEqual("hello", t_music.name)
    def test_studio(self):
        t_studio = Studio(host=self.user)
        self.assertEqual(self.user, t_studio.host)
    def test_participant(self):
        t_p = Participant(participant_user=self.user)
        self.assertEqual(self.user, t_p.participant_user)
    def test_comment(self):
        t_comment = Comment(user_name=self.user)
        self.assertEqual(self.user, t_comment.user_name)
    def test_history(self):
        t_h = History(user=self.user)
        self.assertEqual(self.user, t_h.user)
