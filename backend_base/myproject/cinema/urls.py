from django.urls import path, include
from .views import ProtectedHelloView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedHelloView.as_view(), name='protected_hello'),
    path('', include(router.urls)),
]
