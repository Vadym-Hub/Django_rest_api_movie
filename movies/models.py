from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    """Категорії"""
    name = models.CharField("категорія", max_length=150)
    description = models.TextField("опис")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категорія"
        verbose_name_plural = "категорії"


class Actor(models.Model):
    """Актори та режисери"""
    name = models.CharField("імя", max_length=100)
    age = models.PositiveSmallIntegerField("вік", default=0)
    description = models.TextField("опис")
    image = models.ImageField("зображення", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "актори та режисери"
        verbose_name_plural = "актори та режисери"


class Genre(models.Model):
    """Жанри"""
    name = models.CharField("імя", max_length=100)
    description = models.TextField("опис")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанри"


class Movie(models.Model):
    """Фільм"""
    title = models.CharField("назва", max_length=100)
    tagline = models.CharField("слоган", max_length=100, default='')
    description = models.TextField("опис")
    poster = models.ImageField("постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("дата виходу", default=2019)
    country = models.CharField("країна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режисер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актори", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанри")
    world_premiere = models.DateField("примєра у світі", default=date.today)
    budget = models.PositiveIntegerField("бюджет", default=0, help_text="вказати суму в долларах")
    fees_in_usa = models.PositiveIntegerField("збори в США", default=0, help_text="вказати суму в долларах")
    fess_in_world = models.PositiveIntegerField("збори у світі", default=0, help_text="вказати суму в долларах")
    category = models.ForeignKey(Category, verbose_name="категорія", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("чорнетка", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "фільм"
        verbose_name_plural = "фільми"


class MovieShots(models.Model):
    """Кадри із фільму"""
    title = models.CharField("заголовок", max_length=100)
    description = models.TextField("опис")
    image = models.ImageField("картинка", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="фільм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "кадр із фільму"
        verbose_name_plural = "кадри із фільму"


class RatingStar(models.Model):
    """Зірка рейтингу"""
    value = models.SmallIntegerField("значення", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "зірка рейтингу"
        verbose_name_plural = "зірки рейтингу"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адреса", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="зірка")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фільм")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"


class Review(models.Model):
    """Відгуки"""
    email = models.EmailField()
    name = models.CharField("імя", max_length=100)
    text = models.TextField("повідомлення", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="батько", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="фільм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "відгук"
        verbose_name_plural = "відгуки"
