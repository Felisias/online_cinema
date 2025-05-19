import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
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
from rest_framework.permissions import AllowAny

import requests
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

API_URL = "http://localhost:8000/api/token/"


def refresh_access_token(refresh_token, request):
    #response = requests.post('http://127.0.0.1:8000/api/token/refresh/', data={'refresh': refresh_token})
    #if response.status_code == 200:
    #    new_tokens = response.json()
    #    new_access = new_tokens.get('access')
    #    request.session['access_token'] = new_access
    #    return new_access
    #else:
    #    # refresh token тоже невалиден — выходим
    #    request.session.pop('access_token', None)
    #    request.session.pop('refresh_token', None)
    #    return None
    try:
        token = RefreshToken(refresh_token)
        new_access = str(token.access_token)
        request.session['access_token'] = new_access
        return new_access
    except TokenError:
        request.session.pop('access_token', None)
        request.session.pop('refresh_token', None)
        return None

def refresh_token_to_delete(refresh_token, request):
    try:
        token = RefreshToken(refresh_token)
        return token
    except TokenError:
        #request.session.pop('access_token', None)
        #request.session.pop('refresh_token', None)
        return None





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

        if not all([username, email, password]):
            return render(request, 'register.html', {'error': 'Заполните все поля.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email уже зарегистрирован.'})

        user = User.objects.create_user(email=email, username=username, password=password)
        user.save()

        # После регистрации пользователя выполняем аутентификацию через email
        #user = authenticate(request, email=email, password=password)

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
    refresh_token = request.session.get('refresh_token')

    if not access_token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {access_token}'}
    contents = []
    genre_map = {}
    username = None

    try:

        # Получаем имя текущего пользователя
        user_resp = requests.get('http://127.0.0.1:8000/api/user-info/', headers=headers)

        if user_resp.status_code == 401 and refresh_token:
            new_access_token = refresh_access_token(refresh_token, request)
            if new_access_token:
                headers['Authorization'] = f'Bearer {new_access_token}'
                user_resp = requests.get('http://127.0.0.1:8000/api/user-info/', headers=headers)
            else:
                return redirect('login')

        if user_resp.status_code == 200:
            username = user_resp.json().get('username')
        elif user_resp.status_code == 401:
            request.session.pop('access_token', None)
            request.session.pop('refresh_token', None)
            return redirect('login')

        # Получение контента
        content_response = requests.get('http://127.0.0.1:8000/api/contents/', headers=headers)
        if content_response.status_code == 200:
            contents = content_response.json()
        elif content_response.status_code == 401:
            return redirect('login')
        else:
            print(f"Ошибка при получении контента: {content_response.status_code} — {content_response.text}")

        # Получение жанров
        genres_response = requests.get('http://127.0.0.1:8000/api/genres/', headers=headers)
        if genres_response.status_code == 200:
            genres = genres_response.json()
            genre_map = {g['id']: g['name'] for g in genres}
        else:
            print(f"Ошибка при получении жанров: {genres_response.status_code} — {genres_response.text}")

    except requests.exceptions.RequestException as e:
        print("Ошибка соединения с API:", e)

    return render(request, 'home.html', {
        'contents': contents,
        'genre_map': genre_map,
        'username': username,
        'access_token': access_token,
        'refresh_token': refresh_token
    })





def content_detail_view(request, content_id):
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')

    #if not access_token:
    #    return redirect('login')

    headers = {'Authorization': f'Bearer {access_token}'}
    content_data = None
    movie_data = None
    reviews = []
    username = None

    try:
        # Получаем имя текущего пользователя
        user_resp = requests.get('http://127.0.0.1:8000/api/user-info/', headers=headers)

        if user_resp.status_code == 401 and refresh_token:
            new_access_token = refresh_access_token(refresh_token, request)
            if new_access_token:
                headers['Authorization'] = f'Bearer {new_access_token}'
                user_resp = requests.get('http://127.0.0.1:8000/api/user-info/', headers=headers)
            else:
                return redirect('login')


        if user_resp.status_code == 200:
            username = user_resp.json().get('username')
        elif user_resp.status_code == 401:
            request.session.pop('access_token', None)
            request.session.pop('refresh_token', None)
            return redirect('login')

        # Получение контента
        content_resp = requests.get(f'http://127.0.0.1:8000/api/contents/{content_id}/', headers=headers)
        if content_resp.status_code == 200:
            content_data = content_resp.json()
        else:
            return HttpResponse("Контент не найден", status=404)

        # Получение жанров
        genres_resp = requests.get('http://127.0.0.1:8000/api/genres/', headers=headers)
        genre_map = {g['id']: g['name'] for g in genres_resp.json()} if genres_resp.status_code == 200 else {}

        # Movie-данные
        movie_resp = requests.get(f'http://127.0.0.1:8000/api/movies/{content_id}/', headers=headers)
        if movie_resp.status_code == 200:
            movie_data = movie_resp.json()

        # Получение всех отзывов и фильтрация по content_id
        reviews_resp = requests.get('http://127.0.0.1:8000/api/reviews/', headers=headers)
        if reviews_resp.status_code == 200:
            all_reviews = reviews_resp.json()
            reviews = [r for r in all_reviews if r.get('content') == content_id]

    except requests.exceptions.RequestException as e:
        return HttpResponse("Ошибка соединения с API", status=500)

    return render(request, 'content_detail.html', {
        'content': content_data,
        'movie': movie_data,
        'genre_name': genre_map.get(content_data['genre'], 'Неизвестно'),
        'reviews': reviews,
        'username': username,
        "access_token": access_token,
        "refresh_token": refresh_token
    })






def add_review_view(request, content_id):
    if request.method == 'POST':
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')

        if not access_token:
            return redirect('login')

        headers = {'Authorization': f'Bearer {access_token}'}

        text = request.POST.get('text')
        rating = request.POST.get('rating')
        id = request.POST.get('id')
        print(id)
        try:
            review_data = {
                'content': content_id,
                'text': text,
                'rating': rating
            }

            #response = requests.post('http://127.0.0.1:8000/api/reviews/', json=review_data, headers={
            #    'Authorization': f'Bearer {access_token}',
            #    'Content-Type': 'application/json'
            #})

            response = requests.post('http://127.0.0.1:8000/api/reviews/', json=review_data, headers=headers)


            if response.status_code == 401 and refresh_token:
                new_access_token = refresh_access_token(refresh_token, request)
                if new_access_token:
                    headers['Authorization'] = f'Bearer {new_access_token}'
                    response = requests.post('http://127.0.0.1:8000/api/reviews/', json=review_data, headers=headers)
                else:
                    return redirect('login')


            if response.status_code in [200, 201]:
                return redirect('content_detail', content_id=content_id)
            else:
                return HttpResponse("Ошибка при отправке отзыва", status=response.status_code)


        except requests.exceptions.RequestException as e:
            return HttpResponse("Ошибка соединения", status=500)

    return redirect('content_detail', content_id=content_id)



#####class TokenBlacklistView(APIView):
#####    permission_classes = [AllowAny]
#####
#####    def post(self, request):
#####        refresh_token = request.data.get("refresh")
#####
#####        if not refresh_token:
#####            return Response({"error": "No refresh token provided"}, status=400)
#####
#####        token = refresh_token_to_delete(refresh_token, request)
#####
#####        if token is None:
#####            return Response({"error": "Invalid or expired refresh token"}, status=400)
#####
#####        try:
#####            token.blacklist()
#####
#####            #request.session.pop('access_token', None)
#####            #request.session.pop('refresh_token', None)
#####
#####        except AttributeError:
#####            return Response({"error": "Token does not support blacklisting"}, status=400)
#####
#####        return Response(status=205)





def logout_view(request):
    refresh_token = request.session.get('refresh_token')

    if refresh_token:
        try:
            response = requests.post('http://127.0.0.1:8000/api/logout/', json={'refresh': refresh_token})
        except requests.exceptions.RequestException:
            pass

    request.session.flush()

    return redirect('login')


#####class UserViewSet(viewsets.ModelViewSet):
#####    queryset = User.objects.all()
#####    serializer_class = UserSerializer
#####    permission_classes = [IsAuthenticatedOrReadOnly]


#####class UserRegisterView(generics.CreateAPIView):
#####    queryset = User.objects.all()
#####    serializer_class = UserRegistrationSerializer


#####class GenreViewSet(viewsets.ModelViewSet):
#####    queryset = Genre.objects.all()
#####    serializer_class = GenreSerializer
#####    permission_classes = [IsAuthenticatedOrReadOnly]


#####class ContentViewSet(viewsets.ModelViewSet):
#####    queryset = Content.objects.all()
#####    serializer_class = ContentSerializer
#####    permission_classes = [IsAuthenticatedOrReadOnly]


#####class MovieViewSet(viewsets.ModelViewSet):
#####    queryset = Movie.objects.all()
#####    serializer_class = MovieSerializer
#####    permission_classes = [IsAuthenticatedOrReadOnly]


#####class SeriesViewSet(viewsets.ModelViewSet):
#####    queryset = Series.objects.all()
#####    serializer_class = SeriesSerializer
#####    permission_classes = [IsAuthenticatedOrReadOnly]


#####class SeasonViewSet(viewsets.ModelViewSet):
#####    queryset = Season.objects.all()
#####    serializer_class = SeasonSerializer
#####    permission_classes = [IsAuthenticatedOrReadOnly]


#####class EpisodeViewSet(viewsets.ModelViewSet):
#####    queryset = Episode.objects.all()
#####    serializer_class = EpisodeSerializer
#####    permission_classes = [IsAuthenticatedOrReadOnly]


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

#####class ReviewViewSet(viewsets.ModelViewSet):
#####    queryset = Review.objects.all()
#####    serializer_class = ReviewSerializer
#####    permission_classes = [IsAuthenticatedOrReadOnly]
#####
#####    def get_serializer_context(self):
#####        return {'request': self.request}




#####class ProtectedHelloView(APIView):
#####    permission_classes = [IsAuthenticated]
#####
#####    def get(self, request):
#####        return Response({"message": f"Привет, {request.user.username}. Ты аутентифицирован!"})




#####@api_view(['GET'])
#####@permission_classes([IsAuthenticated])
#####def user_info_view(request):
#####    return Response({
#####        'id': request.user.id,
#####        'username': request.user.username,
#####        'email': request.user.email
#####    })




#####class UserInfoView(APIView):
#####    permission_classes = [IsAuthenticated]
#####
#####    def get(self, request):
#####        return Response({
#####            'id': request.user.id,
#####            'username': request.user.username,
#####            'email': request.user.email
#####        })



#####class ChangePasswordView(APIView):
#####    permission_classes = [IsAuthenticated]
#####
#####    def post(self, request):
#####        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
#####        if serializer.is_valid():
#####            user = request.user
#####            user.set_password(serializer.validated_data['new_password'])
#####            user.save()
#####            return Response({'message': 'Пароль успешно изменён'}, status=status.HTTP_200_OK)
#####        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)