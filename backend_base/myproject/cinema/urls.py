from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    GenreViewSet,
    ContentViewSet,
    MovieViewSet,
    SeriesViewSet,
    SeasonViewSet,
    EpisodeViewSet,
    ReviewViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'series', SeriesViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'episodes', EpisodeViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
