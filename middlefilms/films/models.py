from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime


class Types(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Countries(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def get_absolute_url_film(self):
        return reverse('films_category', kwargs={'slug': self.slug})

    def get_absolute_url_serial(self):
        return reverse('serials_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Genres(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def get_absolute_url_film(self):
        return reverse('films_category', kwargs={'slug': self.slug})

    def get_absolute_url_serial(self):
        return reverse('serials_category', kwargs={'slug': self.slug})

    def get_absolute_url_mult(self):
        return reverse('mults_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Films(models.Model):
    kinopoisk_id = models.IntegerField()
    imdb_id = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    title_original = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='photos/')
    year = models.IntegerField()
    premiere = models.DateField(blank=True, default=datetime.date(2000, 1, 1))
    rating_kp = models.FloatField()
    rating_imdb = models.FloatField(blank=True)
    time = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    type = models.ForeignKey(Types, on_delete=models.PROTECT)
    country = models.ManyToManyField(Countries)
    genres = models.ManyToManyField(Genres)
    produser = models.TextField()
    actors = models.TextField()
    age_restriction = models.IntegerField(blank=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    is_published = models.BooleanField(default=True)
    is_out = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('film', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-created_at']


class Comments(models.Model):
    film = models.ForeignKey(Films, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий к фильму {self.film.title} № {self.id}'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Films, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рейтинги'
        verbose_name_plural = 'Рейтинг'
        ordering = ['-created_at']

    def __str__(self):
        return f'Рейтинг {self.rating} к фильму {self.film.title} от {self.user.get_username()}'


class Slides(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField()
    genres = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='photos/')
    url = models.CharField(max_length=255, default='-')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        ordering = ['number']
