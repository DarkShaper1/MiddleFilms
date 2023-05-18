import random
from django.shortcuts import redirect
from django.shortcuts import render
from .create_films import create_films
from .models import *
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.paginator import Paginator
from django.db.models import Avg

from .forms import CommentForm


def index(request):
    slides = Slides.objects.all().order_by('number')
    film = Films.objects.filter(
        Q(type__title='Фильм') & Q(is_published=True)).order_by('-premiere')[:12]
    serial = Films.objects.filter(
        Q(type__title='Сериал') & Q(is_published=True)).order_by('-premiere')[:12]
    mult = Films.objects.filter(Q(type__title='Мультфильм') & Q(is_published=True)).order_by('-premiere')[:12]
    return render(request, 'films/index.html',
                  {'title': 'Главная', 'films': film, 'serials': serial, 'mults': mult, 'slides': slides, })


@require_http_methods(['GET'])
def ajax_index(request):
    get_req_order = request.GET.get('order')
    get_req_type = request.GET.get('type')

    if get_req_type is not None and get_req_order is not None:
        films = Films.objects.filter(Q(type__title=get_req_type) & Q(is_published=True)).order_by(get_req_order).values(
            'title',
            'rating_kp',
            'rating_imdb',
            'poster',
            'year', 'slug')[:12]
    else:
        films = ''
    response = {'films': list(films), }

    return JsonResponse(response)


@xframe_options_exempt
def get_film(request, slug):
    context = {}
    film = get_object_or_404(Films, slug=slug)
    user = auth.get_user(request)
    context['comments'] = film.comments_set.filter(is_published=True)
    if user.is_authenticated:
        context['form'] = CommentForm
    recomendations = Films.objects.filter(
        Q(genres=film.genres.first()) & ~Q(slug=slug) & Q(type__id=film.type_id) & Q(is_published=True)).order_by('?')[
                     :6]
    context['film'] = film
    context['recs'] = recomendations
    rating = Rating.objects.filter(film=film).aggregate(Avg('rating'))['rating__avg']
    if rating is not None:
        context['rating'] = rating
    else:
        context['rating'] = 0.0
    try:
        your_rating = Rating.objects.get(film=film, user=user).rating
        context['your_rating'] = your_rating
    except:
        print('error')
    return render(request, 'films/film.html', context)


def show_films(request, type_name, slug=None):
    order = '-year'
    get_params, order_get, country_get, year_get, rating_get = '', '', '', '', ''
    if request.GET.get('order') in ['-views', '-rating_kp', 'title', '-created_at']:
        order = request.GET.get('order')
        order_get = order
        get_params += f'&order={order_get}'
    if slug is not None:
        genre = get_object_or_404(Genres, slug=slug)
        films = Films.objects.filter(
            Q(is_published=True) & Q(type__title=type_name) & Q(genres__slug=slug)).order_by(order, '-premiere')
    else:
        films = Films.objects.filter(
            Q(is_published=True) & Q(type__title=type_name)).order_by(order, '-premiere')
    years = list(films.order_by().values_list('year', flat=True).order_by('-year').distinct())
    countries = list(films.values_list('country__title', 'country__slug').order_by('country__title').distinct())
    countries_slug = list(films.values_list('country__slug', flat=True).order_by('country__title').distinct())
    year_req = request.GET.get('year')
    if year_req is not None:
        if year_req.isdigit():
            if int(year_req) in years:
                films = films.filter(year=year_req)
                year_get = int(year_req)
                get_params += f'&year={year_get}'
    if request.GET.get('country') in countries_slug:
        films = films.filter(country__slug=request.GET.get('country'))
        country_get = request.GET.get('country')
        get_params += f'&country={country_get}'
    rating_req = request.GET.get('rating')
    if rating_req is not None:
        if rating_req.isdigit():
            films = films.filter(rating_kp__gte=rating_req)
            rating_get = rating_req
            get_params += f'&rating={rating_get}'

    pag = Paginator(films, 24)
    page_number = request.GET.get('page')
    page_obj = pag.get_page(page_number)
    films_count = pag.count
    page_count = pag.num_pages
    return render(request, 'films/category.html',
                  {'films': page_obj, 'title': str(type_name) + 'ы', 'years': years,
                   'countries': countries, 'films_count': films_count, 'page_count': page_count,
                   'rating_get': rating_get, 'year_get': year_get, 'order_get': order_get, 'country_get': country_get,
                   'get_params': get_params})


@login_required
@require_http_methods(['POST'])
def add_comment(request, film_id):
    form = CommentForm(request.POST)
    film = get_object_or_404(Films, id=film_id)

    if form.is_valid():
        comment = Comments()
        comment.film = film
        comment.user = auth.get_user(request)
        comment.content = form.cleaned_data['comment_area']
        comment.save()
    return redirect(film.get_absolute_url())


@require_http_methods(['GET'])
def add_rating(request, film_id):
    film = get_object_or_404(Films, id=film_id)
    rating = request.GET.get('rating')
    if rating is not None:
        user = auth.get_user(request)
        if user.is_authenticated:
            obj, created = Rating.objects.update_or_create(user=user, film=film, defaults={'rating': rating})
            rating_of_film = Rating.objects.filter(film=film).aggregate(Avg('rating'))
            response = {'your_rating': 'Ваша оценка: ' + rating, 'avg_rating': rating_of_film}
        else:
            rating_of_film = Rating.objects.filter(film=film).aggregate(Avg('rating'))
            response = {'your_rating': 'Вы не авторизированы', 'avg_rating': rating_of_film}
    else:
        response = {'error': 'error',}
    return JsonResponse(response)


def search_films(request):
    query = request.GET.get('search')
    query_cap = query.capitalize()
    films = Films.objects.filter(Q(title__icontains=query_cap) & Q(is_published=True)).order_by('title')

    pag = Paginator(films, 24)
    page_number = request.GET.get('page')
    page_obj = pag.get_page(page_number)
    films_count = pag.count
    page_count = pag.num_pages
    return render(request, 'films/search.html',
                  {'films': page_obj, 'title': 'Поиск по запросу ' + query, 'films_count': films_count,
                   'page_count': page_count, 'query': query})


def random_film(request):
    films = Films.objects.filter(is_published=True)
    select_page = random.choice(films)
    return redirect(select_page.get_absolute_url())


@login_required
def show_admin_page(request):
    if request.method == 'POST':
        count = request.POST.get('count-films')
        content = create_films(count)
    else:
        content = ''
    errors_producer = Films.objects.filter(produser='')
    errors_actors = Films.objects.filter(actors='')
    return render(request, 'films/custom_admin.html', {
        'content_main': content,
        'errors_producer': errors_producer,
        'errors_actors': errors_actors,
    })
