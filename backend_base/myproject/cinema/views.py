from django.shortcuts import render
from django.views import View

# Create your views here.


from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Movie
#from .serializers import MovieSerializer
from .serializers import FilmSerializer



class FilmListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = FilmSerializer

class FilmRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = FilmSerializer




#@api_view(['POST'])
#def add_movie(request):
#    if request.method == 'POST':
#        serializer = MovieSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Пример GET метода
#class FilmListView(View):
#    def get(self, request):
#        films = Film.objects.all()  # Получаем все фильмы
#        films_data = [{"title": film.title, "genre": film.genre} for film in films]
#        return JsonResponse(films_data, safe=False)
#
## Пример POST метода
#@csrf_exempt  # Это отключит проверку CSRF для этого метода (если это необходимо)
#class FilmCreateView(View):
#    def post(self, request):
#        data = json.loads(request.body)  # Чтение данных из тела запроса
#        film = Film.objects.create(
#            title=data["title"],
#            genre=data["genre"],
#            release_year=data["release_year"]
#        )
#        return JsonResponse({"id": film.id}, status=201)