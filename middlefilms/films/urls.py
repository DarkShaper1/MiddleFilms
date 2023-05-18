from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('order-films/', ajax_index, name='ajax-index'),
    path('search/', search_films, name='search_films'),
    path('customadmin/', show_admin_page, name='custom_admin'),
    path('films/', show_films, {'type_name': 'Фильм'}, name='show_films'),
    path('serials/', show_films, {'type_name': 'Сериал'}, name='show_serials'),
    path('mults/', show_films, {'type_name': 'Мультфильм'}, name='show_mults'),
    path('comments/<int:film_id>', add_comment, name='add_comment'),
    path('rating/<int:film_id>', add_rating, name='add_rating'),
    path('films/<str:slug>', show_films, {'type_name': 'Фильм'}, name='films_category'),
    path('serials/<str:slug>', show_films, {'type_name': 'Сериал'}, name='serials_category'),
    path('randompage/', random_film, name='random_film'),
    path('<str:slug>/', get_film, name='film'),
]
