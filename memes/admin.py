from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import Memes, Category, Comments


@admin.register(Memes)
class MemesAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'get_html_photo')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'date', 'cat', 'slug', 'get_html_photo')
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        return mark_safe(f"<img src='{object.img.url}' width=50>")

    get_html_photo.short_description =  'Микро мем'

@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'mem')