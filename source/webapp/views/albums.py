from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy
from webapp.models import Album, FavoriteAlbum
from webapp.forms import AlbumForm
from django.views.generic.edit import FormMixin


class AlbumDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Album
    template_name = 'albums/album_view.html'
    form_class = None

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = DetailView.get_context_data(self, object=self.object)
        try:
            if self.object.fav_album.filter(user=self.request.user):
                context['is_fav'] = True
            else:
                context['is_fav'] = False
        except TypeError:
            return self.render_to_response(context)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs) :
        self.object = self.get_object()
        if FavoriteAlbum.objects.filter(user=self.request.user):
            fav = FavoriteAlbum.objects.filter(user=self.request.user)
            fav.delete()
        else:
            fav = FavoriteAlbum()
            fav.user = self.request.user
            fav.album = self.object
            fav.save()
        return redirect('images:album-detail',self.kwargs.get('pk'))

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
