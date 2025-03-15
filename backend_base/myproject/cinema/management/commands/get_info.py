from django.core.management.base import BaseCommand
from cinema.models import Content

class Command(BaseCommand):
    help = "Вывести контент по указанному режиссёру"

    def add_arguments(self, parser):
        parser.add_argument("director_name", type=str, help="Имя режиссёра для поиска контента")

    def handle(self, *args, **options):
        director_name = options["director_name"]
        contents = Content.objects.filter(director=director_name)

        if contents.exists():
            self.stdout.write(self.style.SUCCESS(f'Контент с режиссёром {director_name}:'))
            for content in contents:
                self.stdout.write(f"ID: {content.id}, Название: {content.title}, Жанр: {content.genre.name}, Возрастной рейтинг: {content.age_rating}")
        else:
            self.stdout.write(self.style.WARNING(f'Нет контента с режиссёром {director_name}'))
