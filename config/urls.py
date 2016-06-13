"""
musicgreed URL Configuration

"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^', include('apps.music.urls', namespace='music')),
    url(r'^admin/', admin.site.urls),
]
