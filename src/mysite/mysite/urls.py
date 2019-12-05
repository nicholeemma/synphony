from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

'''

Url routing for the whole app

'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),#Gmail
    url(r'^', include('synphony.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
