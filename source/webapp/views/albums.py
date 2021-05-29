from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy
from webapp.models import Album
from webapp.forms import AlbumForm


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'albums/album_view.html'

class AlbumAddView(LoginRequiredMixin, CreateView):
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

class AlbumUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = AlbumForm
    model = Album
    template_name = 'albums/album_update_view.html'
    context_object_name = 'album'
    permission_required = 'webapp.change_album'

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def get_success_url(self):
        return reverse('images:album-detail', kwargs={'pk': self.kwargs.get('pk')})

class AlbumDeleteView( DeleteView):
    model = Album
    context_object_name = 'album'
    success_url = reverse_lazy('images:index')
    permission_required = 'webapp.delete_image'

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
