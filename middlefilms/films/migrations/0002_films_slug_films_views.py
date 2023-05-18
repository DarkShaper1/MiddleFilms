# Generated by Django 4.1.2 on 2022-10-27 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='films',
            name='slug',
            field=models.SlugField(default=0, max_length=255, unique=True, verbose_name='Url'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='films',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Кол-во просмотров'),
        ),
    ]