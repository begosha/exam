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


class IndexView(ListView):

    template_name = 'images/index.html'
    model = Image
    context_object_name = 'images'
    ordering = ('-created_at',)
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()

        return super(IndexView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(title__icontains=self.search_data) |
                Q(author__icontains=self.search_data) |
                Q(content__icontains=self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})
        return context

class ImageDetailView(DetailView):
    model = Image
    template_name = 'images/image_view.html'

class ImageAddView(CreateView):
    template_name = 'images/image_add_view.html'
    form_class = ImageForm
    model = Image


    def form_valid(self, form):
        image = form.save(commit=False)
        image.author = self.request.user
        image.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('images:index')

class ImageUpdateView(UpdateView):
    form_class = ImageForm
    model = Image
    template_name = 'images/image_update_view.html'
    context_object_name = 'image'

    def get_success_url(self):
        return reverse('images:image-detail', kwargs={'pk': self.kwargs.get('pk')})