import random
import string
from django.core.management.base import BaseCommand
from cinema.models import Movie, Content, Genre, User
from datetime import datetime


def generate_random_string(length=8):
    """Генерация случайного названия"""
    return ''.join(random.choices(string.ascii_letters + " ", k=length))


class Command(BaseCommand):
    help = 'Populate database with random movies'

    def handle(self, *args, **kwargs):
        genres = list(Genre.objects.all())
        users = list(User.objects.all())

        if not genres:
            self.stdout.write(self.style.ERROR('No genres found. Run python manage.py populate_genres'))
            return

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Run python manage.py populate_users'))
            return

        for _ in range(10):
            title = generate_random_string(random.randint(8, 20))
            director = generate_random_string(10)
            age_rating = random.choice([0, 6, 12, 16, 18])
            genre = random.choice(genres)

            content = Content.objects.create(
                genre=genre,
                title=title,
                director=director,
                age_rating=age_rating
            )

            Movie.objects.create(
                content=content,
                duration=random.randint(60, 180),
                release_date=datetime(2023, random.randint(1, 12), random.randint(1, 28)),
                file_path=f"/movies/{title.replace(' ', '_')}.mp4"
            )

        self.stdout.write(self.style.SUCCESS('Successfully created random movies'))
