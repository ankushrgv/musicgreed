from django import forms

class EditTrackForm(forms.Form):
	title = forms.CharField()
	artist = forms.CharField()
	album = forms.CharField()
	genre = forms.CharField()
	rating = forms.IntegerField()
	trackid = forms.IntegerField()


class EditArtistForm(forms.Form):
	name = forms.CharField()

class EditGenreForm(forms.Form):
	genre = forms.CharField()

class EditAlbumForm(forms.Form):
	album = forms.CharField()
	artist = forms.CharField()