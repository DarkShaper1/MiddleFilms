# Generated by Django 4.1.2 on 2022-11-01 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0005_films_premiere'),
    ]

    operations = [
        migrations.AddField(
            model_name='films',
            name='age_restriction',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]