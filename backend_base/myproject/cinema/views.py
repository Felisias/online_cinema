import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from .forms import LoginForm
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
    ChangePasswordSerializer,
    UserRegistrationSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

import requests
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect

API_URL = "http://localhost:8000/api/token/"


def login_view(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        password = request.POST.get('password')

        # Отправляем данные на JWT-эндпоинт
        response = requests.post(API_URL, data={
            'email': username ,
            'password': password
        })

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            refresh_token = tokens['refresh']

            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token

            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([email, password]):
            return render(request, 'register.html', {'error': 'Заполните все поля.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email уже зарегистрирован.'})

        user = User.objects.create_user(email=email, username=username, password=password)
        user.save()

        # После регистрации пользователя выполняем аутентификацию через email
        user = authenticate(request, email=email, password=password)

        # Получаем токен, как в login_view
        response = requests.post(API_URL, data={
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            refresh_token = tokens['refresh']

            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            return redirect('home')
        else:
            return render(request, 'register.html', {'error': 'Регистрация прошла, но вход не выполнен.'})


#        if user is not None:
#            login(request, user)
#            return redirect('/')  # перенаправление на главную
#        else:
#            return render(request, 'register.html', {'error': 'Ошибка аутентификации.'})

    return render(request, 'register.html')





def home_view(request):
    access_token = request.session.get('access_token')

    if not access_token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        response = requests.get('http://127.0.0.1:8000/api/movies/', headers=headers)

        if response.status_code == 200:
            movies = response.json()
        elif response.status_code == 401:
            # Токен недействителен — отправим на логин
            return redirect('login')
        else:
            movies = []
            print(f"Ошибка при получении фильмов: {response.status_code} — {response.text}")

    except requests.exceptions.RequestException as e:
        print("Ошибка соединения с API:", e)
        movies = []

    return render(request, 'home.html', {'movies': movies})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


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



#class ReviewViewSet(viewsets.ModelViewSet):
#    queryset = Review.objects.all()
#    serializer_class = ReviewSerializer
#
#    def get_serializer_context(self):
#        return {'request': self.request}

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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