from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Artist(models.Model):
	name = models.CharField(db_index=True, max_length= 30)
	no_of_tracks = models.IntegerField(default=0)
	no_of_albums = models.IntegerField(default=0)

	def __unicode__(self):
		return u'%s' % self.name

class Album(models.Model):
	name = models.CharField(db_index=True, max_length= 30)
	no_of_tracks = models.IntegerField(default=0)
	artist = models.ForeignKey(Artist, related_name='album_artist')
	release_year = models.DateField()

	def __unicode__(self):
		return u'%s' % self.name	


class Genre(models.Model):
	genre = models.CharField(db_index=True, max_length= 30)
	no_of_tracks = models.IntegerField(default=0)
	no_of_artists = models.IntegerField(default=0)

	def __unicode__(self):
		return u'%s' % self.genre

class Track(models.Model):
	title = models.CharField(db_index=True, max_length= 50)
	genre = models.ForeignKey(Genre, related_name='track_genre')
	artist = models.ForeignKey(Artist, related_name='artist')
	rating = models.IntegerField(default = 0)
	album = models.ForeignKey(Album, related_name='album')

	def __unicode__(self):
		return u'%s' % self.title