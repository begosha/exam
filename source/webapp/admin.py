from django.contrib import admin
from .models import Album, Image, FavoriteImage, FavoriteAlbum, TokenImage


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


class FavoriteImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'user']
    list_filter = ['user']
    search_fields = ['user']
    fields = ['id', 'image', 'user']
    readonly_fields = ['id']

class FavoriteAlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'album', 'user']
    list_filter = ['user']
    search_fields = ['user']
    fields = ['id', 'album', 'user']
    readonly_fields = ['id']

class TokenImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'token']
    list_filter = ['image']
    search_fields = ['image']
    fields = ['id', 'image', 'token']
    readonly_fields = ['id']
admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(FavoriteAlbum, FavoriteAlbumAdmin)
admin.site.register(FavoriteImage, FavoriteImageAdmin)
admin.site.register(TokenImage, TokenImageAdmin)