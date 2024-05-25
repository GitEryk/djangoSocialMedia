from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'slug', 'description', 'created', 'user']
    list_filter = ['created', 'user']
