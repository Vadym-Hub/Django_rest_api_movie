# Generated by Django 3.0.8 on 2020-07-17 01:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='імя')),
                ('age', models.PositiveSmallIntegerField(default=0, verbose_name='вік')),
                ('description', models.TextField(verbose_name='опис')),
                ('image', models.ImageField(upload_to='actors/', verbose_name='зображення')),
            ],
            options={
                'verbose_name': 'актори та режисери',
                'verbose_name_plural': 'актори та режисери',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='категорія')),
                ('description', models.TextField(verbose_name='опис')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'категорія',
                'verbose_name_plural': 'категорії',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='імя')),
                ('description', models.TextField(verbose_name='опис')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'жанри',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='назва')),
                ('tagline', models.CharField(default='', max_length=100, verbose_name='слоган')),
                ('description', models.TextField(verbose_name='опис')),
                ('poster', models.ImageField(upload_to='movies/', verbose_name='постер')),
                ('year', models.PositiveSmallIntegerField(default=2019, verbose_name='дата виходу')),
                ('country', models.CharField(max_length=30, verbose_name='країна')),
                ('world_premiere', models.DateField(default=datetime.date.today, verbose_name='примєра у світі')),
                ('budget', models.PositiveIntegerField(default=0, help_text='вказати суму в долларах', verbose_name='бюджет')),
                ('fees_in_usa', models.PositiveIntegerField(default=0, help_text='вказати суму в долларах', verbose_name='збори в США')),
                ('fess_in_world', models.PositiveIntegerField(default=0, help_text='вказати суму в долларах', verbose_name='збори у світі')),
                ('url', models.SlugField(max_length=130, unique=True)),
                ('draft', models.BooleanField(default=False, verbose_name='чорнетка')),
                ('actors', models.ManyToManyField(related_name='film_actor', to='movies.Actor', verbose_name='актори')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='movies.Category', verbose_name='категорія')),
                ('directors', models.ManyToManyField(related_name='film_director', to='movies.Actor', verbose_name='режисер')),
                ('genres', models.ManyToManyField(to='movies.Genre', verbose_name='жанри')),
            ],
            options={
                'verbose_name': 'фільм',
                'verbose_name_plural': 'фільми',
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='значення')),
            ],
            options={
                'verbose_name': 'зірка рейтингу',
                'verbose_name_plural': 'зірки рейтингу',
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, verbose_name='імя')),
                ('text', models.TextField(max_length=5000, verbose_name='повідомлення')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie', verbose_name='фільм')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='movies.Review', verbose_name='батько')),
            ],
            options={
                'verbose_name': 'відгук',
                'verbose_name_plural': 'відгуки',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, verbose_name='IP адреса')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie', verbose_name='фільм')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.RatingStar', verbose_name='зірка')),
            ],
            options={
                'verbose_name': 'рейтинг',
                'verbose_name_plural': 'рейтинги',
            },
        ),
        migrations.CreateModel(
            name='MovieShots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='заголовок')),
                ('description', models.TextField(verbose_name='опис')),
                ('image', models.ImageField(upload_to='movie_shots/', verbose_name='картинка')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie', verbose_name='фільм')),
            ],
            options={
                'verbose_name': 'кадр із фильму',
                'verbose_name_plural': 'кадри із фильму',
            },
        ),
    ]