from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings


HOMEPAGE_URL = 'gallery/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=HOMEPAGE_URL, permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
]
