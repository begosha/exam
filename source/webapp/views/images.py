from rest_framework.authtoken.models import Token

from webapp.models import Image
from webapp.forms import SearchForm, ImageForm, AlbumForm
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


class IndexView(LoginRequiredMixin,ListView):

    template_name = 'images/index.html'
    model = Image
    context_object_name = 'images'
    ordering = ('-created_at',)
    paginate_by = 5
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'images':Image.objects.filter(Q(is_public=True) | Q(author=self.request.user))
        }
        )
        return context

class ImageDetailView(LoginRequiredMixin, DetailView):
    model = Image
    template_name = 'images/image_view.html'

class ImageAddView(LoginRequiredMixin, CreateView):
    template_name = 'images/image_add_view.html'
    model = Image
    form_class = ImageForm
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ImageAddView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        image = form.save(commit=False)
        image.author = self.request.user
        image.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('images:index')

class ImageUpdateView(PermissionRequiredMixin,UpdateView):
    form_class = ImageForm
    model = Image
    template_name = 'images/image_update_view.html'
    context_object_name = 'image'
    permission_required = 'webapp.change_image'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ImageUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def get_success_url(self):
        return reverse('images:image-detail', kwargs={'pk': self.kwargs.get('pk')})

class ImageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Image
    context_object_name = 'image'
    success_url = reverse_lazy('images:index')
    permission_required = 'webapp.delete_image'

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
