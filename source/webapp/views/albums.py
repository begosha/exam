from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.edit import FormMixin
import json
from webapp.models import Album
from webapp.forms import AlbumForm

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/album_view.html'

class AlbumAddView(CreateView):
    template_name = 'albums/album_add_view.html'
    form_class = AlbumForm
    model = Album


    def form_valid(self, form):
        image = form.save(commit=False)
        image.author = self.request.user
        image.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('images:index')

class AlbumUpdateView(UpdateView):
    form_class = AlbumForm
    model = Album
    template_name = 'albums/album_update_view.html'
    context_object_name = 'album'

    def get_success_url(self):
        return reverse('images:album-detail', kwargs={'pk': self.kwargs.get('pk')})

class AlbumDeleteView( DeleteView):
    model = Album
    context_object_name = 'album'
    success_url = reverse_lazy('images:index')

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
