# chat/urls.py
from django.urls import re_path, path
from synphony import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    url("^(?P<key>[a-f0-9]{16})$", views.index, name = "index"),
    url("^(?P<key>[a-f0-9]{16})/addSongs$", views.addSongsToStudio, name = "addSongs"),
	  url("^(?P<key>[a-f0-9]{16})/deleteSongs$", views.deleteSongsFromPlayList, name = "deleteSongs"),
	  url("^(?P<key>[a-f0-9]{16})/likeSongs$", views.likeSongsFromPlayList, name = "likeSongs"),
    re_path(r'signup', views.signup, name='signup'),
    re_path(r'login', views.user_login, name='login'),
    re_path(r'logout', views.user_logout, name='logout'),
    re_path(r'studio', views.studio_view, name='studio')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if not settings.DEBUG:
#     urlpatterns += [
#         url(r'^uploads/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
#         url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
#     ]
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
