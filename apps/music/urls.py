from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$',views.TrackList.as_view(), name='track'),
    url(r'^track$',views.TrackList.as_view(), name='track'),
    url(r'^artist$',views.ArtistList.as_view(), name='artist'),
    url(r'^genre$',views.GenreList.as_view(), name='genre'),
    url(r'^album$',views.AlbumList.as_view(), name='genre'),
    url(r'^track/(?P<pk>[\d]+)/$',views.TrackDetails.as_view(), name='trackdetails'),
    url(r'^artist/(?P<pk>\d+)/$',views.ArtistDetails.as_view(), name='artistdetails'),
    url(r'^genre/(?P<pk>\d+)/$',views.GenreDetails.as_view(), name='genredetails'),
    url(r'^album/(?P<pk>\d+)/$',views.AlbumDetails.as_view(), name='albumdetails'),
    url(r'^addnew_form_submit/$', views.AddNew, name="addnew"),
]