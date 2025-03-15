import random
import string
from django.core.management.base import BaseCommand
from cinema.models import User


def generate_random_email():
    """Генерация случайного email"""
    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{name}@mail.ru"


def generate_random_string(length=8):
    """Генерация случайной строки"""
    return ''.join(random.choices(string.ascii_letters, k=length))


class Command(BaseCommand):
    help = 'Populate database with random users'

    def handle(self, *args, **kwargs):
        for _ in range(10):
            email = generate_random_email()
            username = generate_random_string(10)
            password = "password123"  # Можно заменить на `generate_random_string(12)`
            User.objects.create_user(email=email, username=username, password=password)

        self.stdout.write(self.style.SUCCESS('Successfully created random users'))
