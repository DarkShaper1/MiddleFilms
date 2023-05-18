from django import template
from films.models import Films
from django.db.models import Q

register = template.Library()


@register.inclusion_tag('films/menu_tpl.html')
def show_menu(menu_class):
    films = Films.objects.filter(
        Q(is_published=True) & Q(type__title='Фильм'))
    serials = Films.objects.filter(
        Q(is_published=True) & Q(type__title='Сериал'))
    genres_films = films.values_list('genres__title', 'genres__slug').order_by(
        'genres__title').distinct()
    genres_serials = serials.values_list('genres__title', 'genres__slug').order_by(
        'genres__title').distinct()
    return {'genres_films': genres_films, 'genres_serials': genres_serials, 'class': menu_class}
