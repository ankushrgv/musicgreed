

from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView, View
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from .models import Genre, Artist, Track, Album
from .forms import EditTrackForm, EditArtistForm, EditAlbumForm, EditGenreForm 

import json
import requests
import urllib

class TrackList(ListView):
	model = Track
	template_name = "music/index.html"

	def get_context_data(self, **kwargs):

		context = super(TrackList, self).get_context_data(**kwargs)
		page_no = self.request.GET.get('page', 1)

		searched_string = self.request.GET.get('searched', None)
		searched_type = self.request.GET.get('search-type', None)
		
		if searched_string:
			if searched_type == 'title':
				results = Track.objects.filter(title__icontains=searched_string)
			else:
				genre_obj = None
				try:
					genre_obj = Genre.objects.get(genre = searched_string)
				except:
					pass
				if genre_obj:
					results = Track.objects.filter(genre = genre_obj.id)
				else:
					results = []	
		else:
			results = Track.objects.order_by('title').all()
		
		tab_categ = 'track'

		p = Paginator(results, settings.PAGINATION_STEP)

		context['page'] = p.page(page_no)
		context['paginator'] = p
		context['tab_categ'] = tab_categ
		context['tabtypes'] = ['track','artist','genre','album']

		return context

class ArtistList(ListView):
	model = Artist
	template_name = "music/index.html"

	def get_context_data(self, **kwargs):

		context = super(ArtistList, self).get_context_data(**kwargs)
		page_no = self.request.GET.get('page', 1)

		searched_string = self.request.GET.get('searched', None)
		
		if searched_string:
			results = Artist.objects.filter(name__icontains=searched_string)
		else:
			results = Artist.objects.order_by('name').all()
	
		tab_categ = 'artist'

		p = Paginator(results, settings.PAGINATION_STEP)

		context['page'] = p.page(page_no)
		context['paginator'] = p
		context['tab_categ'] = tab_categ
		context['tabtypes'] = ['track','artist','genre','album']

		return context


class GenreList(ListView):
	model = Genre
	template_name = "music/index.html"

	def get_context_data(self, **kwargs):

		context = super(GenreList, self).get_context_data(**kwargs)
		page_no = self.request.GET.get('page', 1)

		searched_string = self.request.GET.get('searched', None)
		
		if searched_string:
			results = Genre.objects.filter(genre__icontains=searched_string)
		else:
			results = Genre.objects.order_by('genre').all()

		tab_categ = 'genre'

		p = Paginator(results, settings.PAGINATION_STEP)

		context['page'] = p.page(page_no)
		context['paginator'] = p
		context['tab_categ'] = tab_categ
		context['tabtypes'] = ['track','artist','genre','album']

		return context


class AlbumList(ListView):
	model = Album
	template_name = "music/index.html"

	def get_context_data(self, **kwargs):

		context = super(AlbumList, self).get_context_data(**kwargs)
		page_no = self.request.GET.get('page', 1)

		searched_string = self.request.GET.get('searched', None)
		
		if searched_string:
			results = Album.objects.filter(name__icontains=searched_string)
		else:
			results = Album.objects.order_by('name').all()

		tab_categ = 'album'

		p = Paginator(results, settings.PAGINATION_STEP)

		context['page'] = p.page(page_no)
		context['paginator'] = p
		context['tab_categ'] = tab_categ
		context['tabtypes'] = ['track','artist','genre','album']

		return context


class TrackDetails(DetailView, FormView):
	model = Track
	template_name = "music/details.html"
	pk_url_kwargs = 'pk'
	form_class = EditTrackForm
	success_url = '/track'

	def post(self, request, *args, **kwargs):
		form = self.request.POST

		flag = 0
		flag_artist = 0
		flag_album = 0
		flag_genre = 0
		
		track_obj = Track.objects.get(id = form['song'])
		# print "album = ", form['album']
		new_track_artist = None
		new_track_album = None
		new_track_genre = None
		
		try:
			new_track_artist = Artist.objects.get(name = form['artist'])
			try:	
				new_track_genre = Genre.objects.get(genre = form['genre'])
				try:	
					new_track_album = Album.objects.get(name = form['album'])
				except:
					flag_album = 1
					print "album error"
					pass
			except:
				flag_genre = 1
				print "genre error"
				pass
		except:
			flag_artist = 1
			print "atist error"
			pass
		
		if new_track_artist and new_track_genre and new_track_album:
			
			if new_track_artist.id == new_track_album.artist.pk:
				flag = 1
				print "Album matches the artist..!!"

			if flag == 1:

				if track_obj.artist.pk != new_track_artist.id:
					new_track_artist.no_of_tracks += 1
					old_track_artist = Artist.objects.get(id = track_obj.artist.pk)
					old_track_artist.no_of_tracks -= 1
					track_obj.artist.pk = new_track_artist.id

					new_track_artist.save()
					old_track_artist.save()

				if track_obj.album.pk != new_track_album.id:
					new_track_album.no_of_tracks += 1
					old_track_album = Album.objects.get(id = track_obj.album.pk)
					old_track_album.no_of_tracks -= 1
					track_obj.album.pk = new_track_album.id

					new_track_album.save()
					old_track_album.save()

				if track_obj.genre.pk != new_track_genre.id:
					new_track_genre.no_of_tracks += 1
					old_track_genre = Genre.objects.get(id = track_obj.genre.pk)
					old_track_genre.no_of_tracks -= 1
					track_obj.genre.pk = new_track_genre.id

					new_track_genre.save()
					old_track_genre.save()

				if track_obj.title != form['title']:
					track_obj.title = form['title']


				if track_obj.rating != form['rating']:
					track_obj.rating = form['rating']

				track_obj.save()

			else:
				print "Woah..Artist and albums dont match!!"

		return self.form_valid(form)

	def form_valid(self, form):
		return HttpResponseRedirect(self.success_url)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		context['tab_categ'] = 'track'
		return self.render_to_response(context)
		
	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg)

		if pk is not None:
			queryset = queryset.filter(pk=pk)
		try:
			obj = queryset.get()
		except queryset.model.DoesNotExist:
			raise Http404(("No %(verbose_name)s found matching the query") %
						  {'verbose_name': queryset.model._meta.verbose_name})
		return obj

	def get_context_data(self, **kwargs):
		context = super(TrackDetails, self).get_context_data(**kwargs)
		if self.object:
			context['object'] = self.object
		return context


class ArtistDetails(DetailView, FormView):
	model = Artist
	template_name = "music/details.html"
	pk_url_kwargs = 'pk'
	form_class = EditArtistForm
	success_url = '/artist'

	def post(self, request, *args, **kwargs):
		form = self.request.POST
		artist_name = form['artist']
		artist_id = form['artist-id']
		
		print "artist_name = ", artist_name

		artist_obj = Artist.objects.get(id = artist_id)
		existing_artist = None
		
		if artist_obj.name != artist_name:
			try:
				existing_artist = Artist.objects.get(name = artist_name)
				print "existing_artist name = ", existing_artist.name
			except:
				pass
			
			if existing_artist is None:
				artist_obj.name = artist_name
				artist_obj.save()

			else:
				print "Artist already exist..!!"
		else:
			print "Same artist"

		return self.form_valid(form)

	def form_valid(self, form):
		return HttpResponseRedirect(self.success_url)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		context['tab_categ'] = 'artist'
		return self.render_to_response(context)
		
	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg)

		if pk is not None:
			queryset = queryset.filter(pk=pk)
		try:
			obj = queryset.get()
		except queryset.model.DoesNotExist:
			raise Http404(("No %(verbose_name)s found matching the query") %
						  {'verbose_name': queryset.model._meta.verbose_name})
		return obj

	def get_context_data(self, **kwargs):
		context = super(ArtistDetails, self).get_context_data(**kwargs)
		if self.object:
			context['object'] = self.object
		return context


class GenreDetails(DetailView, FormView):
	model = Genre
	template_name = "music/details.html"
	pk_url_kwargs = 'pk'
	form_class = EditGenreForm
	success_url = '/genre'

	def post(self, request, *args, **kwargs):
		form = self.request.POST
		genre_name = form['genre']
		genre_id = form['genre-id']
		
		print "genre_name = ", genre_name

		genre_obj = Genre.objects.get(id = genre_id)
		existing_genre = None
		
		if genre_obj.genre != genre_name:
			try:
				existing_genre = Genre.objects.get(genre = genre_name)
				print "existing_genre name = ", existing_genre.genre
			except:
				pass
			
			if existing_genre is None:
				genre_obj.genre = genre_name
				genre_obj.save()

			else:
				print "Genre already exist..!!"
		else:
			print "Same Genre"

		return self.form_valid(form)

	def form_valid(self, form):
		return HttpResponseRedirect(self.success_url)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		context['tab_categ'] = 'genre'
		return self.render_to_response(context)
		
	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg)

		if pk is not None:
			queryset = queryset.filter(pk=pk)
		try:
			obj = queryset.get()
		except queryset.model.DoesNotExist:
			raise Http404(("No %(verbose_name)s found matching the query") %
						  {'verbose_name': queryset.model._meta.verbose_name})
		return obj

	def get_context_data(self, **kwargs):
		context = super(GenreDetails, self).get_context_data(**kwargs)
		if self.object:
			context['object'] = self.object
		return context


class AlbumDetails(DetailView, FormView):
	model = Album
	template_name = "music/details.html"
	pk_url_kwargs = 'pk'
	form_class = EditAlbumForm
	success_url = '/album'

	def post(self, request, *args, **kwargs):
		form = self.request.POST
		album_name = form['album']
		album_id = form['album-id']
		album_artist = form['artist']
		
		# print "album_name = ", album_name

		album_obj = Album.objects.get(id = album_id)
		artist_obj = Artist.objects.get(id = album_obj.artist.pk)

		# print "artist_obj = ", artist_obj

		existing_album = None
		existing_artist = None
		
		if artist_obj.name == album_artist:
			if album_obj.name != album_name:
				try:
					existing_album = Album.objects.get(name = album_name)
					print "existing_album name = ", existing_album.name
				except:
					pass
				
				if existing_album is None:
					album_obj.name = album_name
					album_obj.save()

				else:
					print "Album already exist..!!"
			else:
				print "Same Album"

		else:
			try:
				existing_artist = Artist.objects.get(name = album_artist)
			except:
				print "Artist does not exist"

			if existing_artist:
				if album_obj.name != album_name:
					try:
						existing_album = Album.objects.get(name = album_name)
						print "existing_album name = ", existing_album.name
					except:
						pass
					
					if existing_album is None:
						album_obj.name = album_name
						album_obj.save()
					else:
						print "Album already exist..!!"
				
				else:
					print "Same Album with different artist"

				print " old album_obj.artist = ", album_obj.artist
				print "existing_artist = ", existing_artist

				album_obj.artist = existing_artist
				
				print " new album_obj.artist = ", album_obj.artist
				
				artist_obj.no_of_albums -= 1
				artist_obj.no_of_tracks -= album_obj.no_of_tracks

				existing_artist.no_of_albums += 1
				existing_artist.no_of_tracks += album_obj.no_of_tracks

				album_obj.save()
				artist_obj.save()
				existing_artist.save()

		return self.form_valid(form)

	def form_valid(self, form):
		return HttpResponseRedirect(self.success_url)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		context['tab_categ'] = 'album'
		return self.render_to_response(context)
		
	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg)

		if pk is not None:
			queryset = queryset.filter(pk=pk)
		try:
			obj = queryset.get()
		except queryset.model.DoesNotExist:
			raise Http404(("No %(verbose_name)s found matching the query") %
						  {'verbose_name': queryset.model._meta.verbose_name})
		return obj

	def get_context_data(self, **kwargs):
		context = super(AlbumDetails, self).get_context_data(**kwargs)
		if self.object:
			context['object'] = self.object
		return context


def AddNew(request):
	if request.method == 'POST':

		content = request.POST
		print content
		print content['element_type']
		
		if content['element_type'] == 'track':
			track_genre = None
			track_artist = None
			track_album = None
			
			try:
				track_genre = Genre.objects.get(genre = content['genre'])
			except:
				print "Invalid Genre"
				
			try:
				track_artist = Artist.objects.get(name = content['artist'])
			except:
				print "Invalid Artist"

			try:
				track_album = Album.objects.get(name = content['album'])
			except:
				print "Invalid Album"

			if track_genre and track_artist and track_album:
				Track.objects.create(
					title = content['track'],
					genre = track_genre,
					artist = track_artist,
					rating = int(content['rating']),
					album = track_album)

				track_genre.no_of_tracks += 1
				track_artist.no_of_tracks += 1
				track_album.no_of_tracks += 1

				track_genre.save()
				track_artist.save()
				track_album.save()



		elif content['element_type'] == 'artist':
			Artist.objects.create(
				name = content['artist'])

		elif content['element_type'] == 'genre':
			Genre.objects.create(
				genre = content['genre'])

		elif content['element_type'] == 'album':
			album_artist = None
			try:
				album_artist = Artist.objects.get(name = content['artist'])
			except:
				print "Artist doesn't exists!!"

			if album_artist:
				Album.objects.create(
					name = content['album'],
					artist = album_artist)
				album_artist.no_of_albums += 1
				album_artist.save()

		return HttpResponse(
			 json.dumps({'status': 'True'})
		)

	else:
		return HttpResponse(
			json.dumps({"nothing to see": "this ain't happening"})
		)