from django import forms
from django.contrib.auth.models import User
from .models import Music, Studio


class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = [
            'name',
            'description',
            'url',
        ]

class CreateStudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = [
            'name',
            'music',
            'status',
            'host'
        ]
        
