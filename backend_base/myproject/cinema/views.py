from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import (
    User,
    Genre,
    Content,
    Movie,
    Series,
    Season,
    Episode,
    Review
)
from .serializers import (
    UserSerializer,
    GenreSerializer,
    ContentSerializer,
    MovieSerializer,
    SeriesSerializer,
    SeasonSerializer,
    EpisodeSerializer,
    ReviewSerializer,
    ChangePasswordSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


#class ReviewViewSet(viewsets.ModelViewSet):
#    queryset = Review.objects.all()
#    serializer_class = ReviewSerializer
#    permission_classes = [IsAuthenticatedOrReadOnly]



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'request': self.request}



class ProtectedHelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Привет, {request.user.username}. Ты аутентифицирован!"})



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Пароль успешно изменён'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)