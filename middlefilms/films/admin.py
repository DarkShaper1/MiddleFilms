from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class SlidesAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'title')
    list_editable = ('title', 'number')


class GenresAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug')
    list_editable = ('title', 'slug')
    ordering = ('-id',)


class TypesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug')
    list_editable = ('title', 'slug')


class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug')
    list_editable = ('title', 'slug')


class FilmsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title_original',)}
    save_as = True
    save_on_top = True
    list_display = ('get_photo', 'id', 'title', 'slug', 'year', 'type', 'is_published', 'age_restriction')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'kinopoisk_id', 'title_original')
    list_editable = ('is_published', 'slug')
    list_filter = ('genres', 'country', 'year', 'type', 'rating_kp')
    readonly_fields = ('views', 'created_at')

    def get_photo(self, obj):
        if obj.poster:
            return mark_safe(f'<img src="{obj.poster.url}" width="50px">')
        else:
            return '-'

    get_photo.short_description = "Фото"


admin.site.register(Films, FilmsAdmin)
admin.site.register(Types, TypesAdmin)
admin.site.register(Countries, CountryAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Slides, SlidesAdmin)
admin.site.register(Comments)
admin.site.register(Rating)
