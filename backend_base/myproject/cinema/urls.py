from django.urls import path, include
#from .views import ProtectedHelloView
#from .views import ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from rest_framework.routers import DefaultRouter
#from .views import (
    #UserViewSet,
    #ProtectedHelloView,
    #ChangePasswordView,
    #GenreViewSet,
    #ContentViewSet,
    #MovieViewSet,
    #SeriesViewSet,
    #SeasonViewSet,
    #EpisodeViewSet,
    #ReviewViewSet,
    #UserRegisterView,
    #login_view,
    #home_view,
    #register_view,
    #content_detail_view,
    #add_review_view,
    #user_info_view,
    #UserInfoView,
    #TokenBlacklistView,
    #logout_view
#)

from .views_frontend import (
    login_view, register_view, logout_view,
    home_view, content_detail_view, add_review_view
)

from .views_api import (
    ProtectedHelloView, ChangePasswordView, TokenBlacklistView,
    UserRegisterView, UserInfoView, user_info_view,
    UserViewSet, GenreViewSet, ContentViewSet, MovieViewSet,
    SeriesViewSet, SeasonViewSet, EpisodeViewSet, ReviewViewSet
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
    # API endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', ProtectedHelloView.as_view(), name='protected_hello'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/register/', UserRegisterView.as_view(), name='user-register'),
    path('api/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('api/user-info/', user_info_view, name='user_info'),
    path('api/', include(router.urls)),

    # UI (шаблоны)
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('content/<int:content_id>/', content_detail_view, name='content_detail'),
    path('content/<int:content_id>/review/', add_review_view, name='add_review'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
