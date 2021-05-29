from django.contrib.auth import get_user_model
from django.db import models


class Image(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='image',
        null=True
    )

    image = models.ImageField(
        upload_to='images',
        null=False,
        blank=False,
        verbose_name='Image'
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=200,
        verbose_name='Description'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey('webapp.Album', on_delete=models.CASCADE, verbose_name='Album', related_name='image', blank=True)


    class Meta:
        db_table = 'images'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

class Album(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='album',
        null=True
    )
    name = models.CharField(
        null=False,
        blank=False,
        max_length=60,
        verbose_name='Album Name'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Album Description'
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'albums'
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

