from django import forms
from django.contrib.auth import get_user_model

from webapp.models import Album, Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image','description', 'album', 'is_public')

    def __init__(self, user, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['album'] = forms.ModelChoiceField(
            queryset=Album.objects.filter(author=user))

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('name','description', 'is_public')


class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='search')