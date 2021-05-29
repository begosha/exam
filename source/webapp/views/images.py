from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.edit import FormMixin
from rest_framework.authtoken.models import Token
from webapp.models import Image, FavoriteImage, TokenImage
from webapp.forms import ImageForm
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
from django.db.models import Q
from uuid import uuid4


class IndexView(LoginRequiredMixin,ListView):

    template_name = 'images/index.html'
    model = Image
    context_object_name = 'images'
    ordering = ('-created_at',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'images':Image.objects.filter(Q(is_public=True) | Q(author=self.request.user))
        }
        )
        return context

class ImageDetailView(LoginRequiredMixin,FormMixin, DetailView):
    model = Image
    template_name = 'images/image_view.html'
    form_class = None

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = DetailView.get_context_data(self, object=self.object)
        context['token'] = self.request.COOKIES['csrftoken']
        try:
            if self.object.fav_image.filter(user=self.request.user):
                context['is_fav'] = True
            else:
                context['is_fav'] = False
        except TypeError:
            return self.render_to_response(context)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs) :
        self.object = self.get_object()
        if FavoriteImage.objects.filter(user=self.request.user):
            fav = FavoriteImage.objects.filter(user=self.request.user)
            fav.delete()
        else:
            fav = FavoriteImage()
            fav.user = self.request.user
            fav.image = self.object
            fav.save()
        return redirect('image-detail',self.kwargs.get('pk'))

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
        token_image = TokenImage()
        token_image.image = image
        token_image.token = uuid4().hex
        token_image.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')

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
        return reverse('image-detail', kwargs={'pk': self.kwargs.get('pk')})

class ImageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Image
    context_object_name = 'image'
    success_url = reverse_lazy('index')
    permission_required = 'webapp.delete_image'

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
