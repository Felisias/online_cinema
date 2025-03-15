import random
import string
from django.core.management.base import BaseCommand
from cinema.models import Genre, Movie, User
from datetime import datetime


def generate_random_string(length=8):
    """Генерация случайной строки из букв и цифр"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class Command(BaseCommand):
    help = 'Populate the database with random data'

    def handle(self, *args, **kwargs):
        # Создание случайных жанров
        for _ in range(10):  # Например, создаем 10 жанров
            genre_name = generate_random_string(random.randint(5, 15))  # Случайное название жанра
            Genre.objects.get_or_create(name=genre_name)  # get_or_create чтобы избежать дублирования

        # Создание случайных пользователей
        for _ in range(10):  # Например, создаем 10 пользователей
            username = generate_random_string(random.randint(5, 10))  # Случайное имя пользователя
            User.objects.get_or_create(username=username)  # get_or_create чтобы избежать дублирования

        # Создание случайных фильмов
        for _ in range(20):  # Например, создаем 20 фильмов
            title = generate_random_string(random.randint(8, 20))  # Случайное название фильма
            description = generate_random_string(random.randint(20, 100))  # Случайное описание
            genre = random.choice(Genre.objects.all())  # Случайный жанр
            release_date = datetime(2023, random.randint(1, 12), random.randint(1, 28))  # Случайная дата релиза
            created_by = random.choice(User.objects.all())  # Случайный пользователь, создавший фильм

            Movie.objects.create(
                title=title,
                description=description,
                genre=genre,
                release_date=release_date,
                created_by=created_by
            )

        self.stdout.write(self.style.SUCCESS('Database populated with random data.'))
