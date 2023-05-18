import requests
from .models import Films, Countries, Types, Genres
from transliterate import translit
from middlefilms.settings import MEDIA_ROOT

session = requests.Session()
session.headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'


def create_films(count):
    ret = ''
    errors = ''
    file = open('input.txt')
    step = 0
    for i in range(int(count)):
        kp_id = file.readline()
        if not Films.objects.filter(kinopoisk_id=kp_id):
            url = 'https://kinobd.net/api/films/search/kp_id?q=' + str(kp_id)
            req = session.get(url)
            text = req.json()
            text = text['data'][0]
            kpid = text['kinopoisk_id']
            imdbid = str(text['imdb_id'])
            title = text['name_russian']
            if text['name_original'] is None:
                title_original = text['name_russian']
            else:
                title_original = text['name_original']
            poster = text['small_poster']
            yeara = text['year']
            if yeara is not None:
                yeara = yeara[:4]
                year = ''.join([i for i in yeara if i.isdigit()])
            else:
                year = None
            ratingkp = text['rating_kp']
            if text['rating_imdb'] is None:
                ratingimdb = 0
            else:
                ratingimdb = text['rating_imdb']
            time = text['time']
            description = text['description']
            types = text['type']
            age_restriction = text['age_restriction']
            if age_restriction is None:
                age_restriction = 0
            country = text['country_ru']
            genres = text['genres']
            persons = text['persons']
            premiere = text['premiere_world']
            if premiere is None:
                premiere = '2000-01-01'
            acters = ''
            producer = ''
            if text['name_original'] is None:
                slugf = translit(title, "ru", reversed=True)
                slugf = slugf.lower()
                slugf = slugf.replace(' ', '-')
                slugf = slugf.replace(',', '-')
                slugf = slugf.replace('.', '')
                slugf = slugf.replace('«', '')
                slugf = slugf.replace('»', '')
                slugf = slugf.replace(':', '')
                slugf = slugf.replace("'", "")
            else:
                slugf = title_original.replace('-', '')
                slugf = slugf.lower()
                slugf = slugf.replace(',', '-')
                slugf = slugf.replace('.', '')
                slugf = slugf.replace('«', '')
                slugf = slugf.replace('»', '')
                slugf = slugf.replace(' ', '-')
                slugf = slugf.replace("'", "")
                slugf = slugf.replace(':', '')
            if (kpid is not None) and (title is not None) and (poster is not None) and (year is not None) and (
                    ratingkp is not None) and (description is not None) and (types is not None) and (
                    country is not None) and (genres is not None) and (persons is not None) and (
                    acters is not None) and (producer is not None):
                one_film = Films(kinopoisk_id=kpid, slug=slugf)
                one_film.imdb_id = imdbid
                one_film.title = title
                one_film.title_original = title_original
                one_film.year = year
                one_film.premiere = premiere
                one_film.rating_kp = ratingkp
                one_film.rating_imdb = ratingimdb
                one_film.age_restriction = age_restriction
                one_film.time = str(time)
                one_film.description = description
                for pers in persons:
                    if pers['profession']['profession_id'] == 'director':
                        producer = pers['name_russian']
                        break
                profucer_bul = True
                if producer == '':
                    profucer_bul = False
                for pers in persons:
                    if pers['profession']['profession_id'] == 'actor' and pers['name_russian'] != '':
                        acters += str(pers['name_russian']) + ', '
                    if not profucer_bul and pers['profession']['profession_id'] == 'producer' and pers[
                        'name_russian'] != '':
                        producer += str(pers['name_russian']) + ', '
                if not profucer_bul:
                    producer = producer[:-2]
                acters = acters[:-2]
                one_film.actors = acters
                one_film.produser = producer
                mult_bool = False
                for gen in genres:
                    name = gen['name_ru'].capitalize()
                    if name == 'Мультфильм':
                        mult_bool = True
                        break
                if mult_bool:
                    t = Types.objects.get(id=4)
                    one_film.type = t
                elif types == 'film':
                    t = Types.objects.get(id=1)
                    one_film.type = t
                else:
                    t = Types.objects.get(id=2)
                    one_film.type = t
                poster_req = requests.get(poster)
                file_name = title_original.replace(':', '')
                file_name = file_name.replace(' ', '')
                file_name = file_name.replace("'", "")
                file_name = file_name.replace(",", "")
                file_name = file_name.replace("?", "")
                file_name = file_name.replace("!", "")
                with open(f'{MEDIA_ROOT}/photos/{file_name}.jpg', 'wb') as f:
                    f.write(poster_req.content)
                one_film.poster = f'photos/{file_name}.jpg'
                one_film.save()
                one_film = Films.objects.get(kinopoisk_id=kpid)
                for gen in genres:
                    name = gen['name_ru'].capitalize()
                    if not Genres.objects.filter(title=name).exists():
                        name_slug = translit(name, "ru", reversed=True)
                        name_slug = name_slug.replace("'", '')
                        new_gen = Genres(title=name, slug=name_slug.lower())
                        new_gen.save()
                        categ = Genres.objects.get(title=name)
                        one_film.genres.add(categ)
                    else:
                        categ = Genres.objects.get(title=name)
                        one_film.genres.add(categ)
                country = country.replace(' ', '')
                country = country.split(",")
                for c in country:
                    name = c
                    if not Countries.objects.filter(title=name).exists():
                        name_slug = translit(name, "ru", reversed=True)
                        new_gen = Countries(title=name, slug=name_slug.lower())
                        new_gen.save()
                        categ = Countries.objects.get(title=name)
                        one_film.country.add(categ)
                    else:
                        categ = Countries.objects.get(title=name)
                        one_film.country.add(categ)
                ret += '"' + title + '"' + ', '
            else:
                errors += '"' + kp_id + ' ' + str(title) + '"' + ', '
        else:
            errors += '"' + kp_id + '"' + ', '
        # прочитаем файл построчно
        with open('input.txt', 'r') as f:
            lines = f.readlines()

        # запишем файл построчно пропустив первую строку
        with open('input.txt', 'w') as f:
            f.writelines(lines[1:])
        step = i

        # ret = str(kpid) + "\n" + str(imdbid) + '\n' + str(time) +'\n' + str(title) +'\n' + str(title_original) +'\n' + str(poster) +'\n' + str(year) +'\n' + str(ratingkp) +'\n' + str(ratingimdb) +'\n' + str(description) +'\n' + str(types) +'\n' + str(country) +'\n' + str(genres) + '\n' + str(producer) + '\n' + 'Актёры:' +str(acters)
        # return ret
    return f'Были добавлены:{ret} <br><hr>Не были добавлены:  {errors}<hr>'
