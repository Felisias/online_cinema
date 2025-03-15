import random
import string
from django.core.management.base import BaseCommand
from cinema.models import Genre


def generate_random_string(length=8):
    """Генерация случайного названия"""
    return ''.join(random.choices(string.ascii_letters, k=length))


class Command(BaseCommand):
    help = 'Populate database with random genres'

    def handle(self, *args, **kwargs):
        for _ in range(10):
            name = generate_random_string(random.randint(5, 15))
            Genre.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS('Successfully created random genres'))
