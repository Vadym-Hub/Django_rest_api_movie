from django.db import models
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .service import get_client_ip, MovieFilter


class MovieListView(ListAPIView):
    """Вивід списку фільмів"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(RetrieveAPIView):
    """Вивід одного фільму"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(CreateAPIView):
    """Добавлення відгуку до фільму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(CreateAPIView):
    """Добавлення рейтинга фільму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        """Додавання ip користувача, який відправив запрос"""
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(ListAPIView):
    """Вивід списка акторів"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(RetrieveAPIView):
    """Вивід конкретного актора чи режисера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
