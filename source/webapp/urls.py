from django.urls import path
from webapp.views.images import IndexView, ImageDetailView, ImageAddView, ImageUpdateView, ImageDeleteView
from webapp.views.albums import AlbumDetailView, AlbumAddView, AlbumUpdateView, AlbumDeleteView

app_name = 'images'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
    path('<int:pk>/album', AlbumDetailView.as_view(), name='album-detail'),
    path('add/image', ImageAddView.as_view(), name='image-add'),
    path('add/album', AlbumAddView.as_view(), name='album-add'),
    path('<int:pk>/update/', ImageUpdateView.as_view(), name='image-update'),
    path('<int:pk>/update/album', AlbumUpdateView.as_view(), name='album-update'),
    path('<int:pk>/delete/', ImageDeleteView.as_view(), name='image-delete'),
    path('<int:pk>/delete/album', AlbumDeleteView.as_view(), name='album-delete')
]