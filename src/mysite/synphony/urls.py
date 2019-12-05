# synphony/urls.py
from django.urls import re_path, path
from synphony import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    url("^synphony/(?P<key>[a-f0-9]{16})$", views.index, name="index"),
    url("^synphony/(?P<key>[a-f0-9]{16})/deleteSongs$", views.deleteSongsFromPlayList, name="deleteSongs"),
    url("^synphony/(?P<key>[a-f0-9]{16})/likeSongs$", views.likeSongsFromPlayList, name="likeSongs"),
    url("^synphony/(?P<key>[a-f0-9]{16})/closeStudio$", views.closeStudio, name="closeStudio"),
    re_path(r'synphony/signup', views.signup, name='signup'),
    re_path(r'synphony/login', views.user_login, name='login'),
    re_path(r'synphony/logout', views.user_logout, name='logout'),
    re_path(r'synphony/studio', views.studio_view, name='studio'),
    re_path(r'synphony/home', views.home_page, name='home'),
    re_path(r'view_history', views.view_history, name='view_history'),
    re_path(r'.*', views.home_page, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if not settings.DEBUG:
#     urlpatterns += [
#         url(r'^uploads/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
#         url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
#     ]
