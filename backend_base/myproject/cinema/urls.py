from django.urls import path
from .views import FilmListCreateView, FilmRetrieveUpdateDeleteView

urlpatterns = [
    path('films/', FilmListCreateView.as_view(), name='film-list-create'),
    path('films/<int:pk>/', FilmRetrieveUpdateDeleteView.as_view(), name='film-detail'),
]