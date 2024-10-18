from django.db.models import Count, Avg
from rest_framework import generics, views, response, status
from rest_framework.permissions import IsAuthenticated

from app.permissions import GlobalDefaultPermission
from reviews.models import Review
from .models import Movie
from .serializers import MovieSerializer, MovieListRetrieveSerializer


class MovieListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, GlobalDefaultPermission]
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListRetrieveSerializer
        return MovieSerializer


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, GlobalDefaultPermission]
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieListRetrieveSerializer
        return MovieSerializer


class MovieStatsView(views.APIView):
    permission_classes = [IsAuthenticated, GlobalDefaultPermission]
    queryset = Movie.objects.all()

    def get(self, request):
        total_movies = self.queryset.count()
        movies_by_genre = self.queryset.values('genre__name').annotate(count=Count('id'))
        total_reviews = Review.objects.count()
        average_stats = Review.objects.aggregate(avg_stats=Avg('stats'))['avg_stats']

        return response.Response(
            data={
                'total_movies': total_movies,
                'movies_by_genre': movies_by_genre,
                'total_reviews': total_reviews,
                'average_stats': round(average_stats, 1) if average_stats else 0
            },
            status=status.HTTP_200_OK
        )