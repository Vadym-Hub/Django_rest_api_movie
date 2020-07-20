from rest_framework import serializers
from rest_framework.serializers import ListSerializer, Serializer, ModelSerializer

from .models import Movie, Review, Rating, Actor


class FilterReviewListSerializer(ListSerializer):
    """Фільтр коментарів, тільки parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(Serializer):
    """Вивід рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializer(ModelSerializer):
    """Вивід списка акторів та режисерів"""
    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(ModelSerializer):
    """Вивід інформації про конкретного актора чи режисера"""
    class Meta:
        model = Actor
        fields = "__all__"


class MovieListSerializer(ModelSerializer):
    """Список фільмів"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "rating_user", "middle_star")


class ReviewCreateSerializer(ModelSerializer):
    """Додавання відгуку"""

    class Meta:
        model = Review
        fields = "__all__"  # Вивід усіх полів


class ReviewSerializer(ModelSerializer):
    """Вивід відгуку"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class MovieDetailSerializer(ModelSerializer):
    """Один фільм"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft", )  # Вивід усіх полів крім draft


class CreateRatingSerializer(ModelSerializer):
    """Добавлення рейтингу користувачем"""
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(ip=validated_data.get('ip', None),
                                                    movie=validated_data.get('movie', None),
                                                    defaults={'star': validated_data.get('star')})
        return rating
