from django import forms
from webapp.models import Album, Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        album = forms.ModelChoiceField(queryset=Album.objects.all())
        fields = ('image','description', 'album', 'is_public')

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('name','description', 'is_public')
class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')