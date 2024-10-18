from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', views.MovieRetrieveUpdateDestroyView.as_view(), name='movie-detail'),
    path('movies/stats/', views.MovieStatsView.as_view(), name='movie-stats')
]
