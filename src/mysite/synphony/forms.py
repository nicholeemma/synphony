from django import forms
from django.contrib.auth.models import User
from .models import Music


class MusicForm(forms.modelForm):
    class Meta:
        model = Music
        fields = [
            'name',
            'description',
            'url',
        ]
