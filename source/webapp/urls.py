from django.urls import path
from webapp.views.images import IndexView, ImageDetailView, ImageAddView, ImageUpdateView

app_name = 'images'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
    path('add/image', ImageAddView.as_view(), name='image-add'),
    path('<int:pk>/update/', ImageUpdateView.as_view(), name='image-update'),
]