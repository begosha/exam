from django.contrib import admin
from .models import Album, Image


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'description', 'created_at']
    list_filter = ['author', 'name']
    search_fields = ['name', 'description']
    fields =['id', 'name', 'author', 'description', 'created_at']
    readonly_fields = ['created_at', 'id', 'author']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'author', 'description', 'album', 'created_at']
    list_filter = ['author']
    search_fields = ['author', 'description']
    fields = ['id', 'image', 'author', 'description', 'album', 'created_at']
    readonly_fields = ['created_at', 'id', 'author']

admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)