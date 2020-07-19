from django.urls import path

from .views import MovieListView, MovieDetailView

urlpatterns = [
    path("movie/", MovieListView.as_view()),
    path("movie/<int:pk>/", MovieDetailView.as_view()),
]