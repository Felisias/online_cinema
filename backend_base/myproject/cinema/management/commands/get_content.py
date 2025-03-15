from django.core.management.base import BaseCommand
from cinema.models import Content, Movie, Series


class Command(BaseCommand):
    help = "Вывести фильмы и сериалы по указанному режиссёру"

    def add_arguments(self, parser):
        parser.add_argument("director_name", type=str, help="Имя режиссёра для поиска")

    def handle(self, *args, **options):
        director_name = options["director_name"]

        # Найдём контент с указанным режиссёром
        contents = Content.objects.filter(director=director_name)

        if not contents.exists():
            self.stdout.write(self.style.WARNING(f'Нет контента с режиссёром {director_name}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Контент с режиссёром {director_name}:'))

        # Выведем найденные фильмы
        movies = Movie.objects.filter(content__in=contents)
        if movies.exists():
            self.stdout.write(self.style.SUCCESS("Фильмы:"))
            for movie in movies:
                self.stdout.write(
                    f"  - {movie.content.title}, Длительность: {movie.duration} минут, Дата выхода: {movie.release_date}")

        # Выведем найденные сериалы
        series = Series.objects.filter(content__in=contents)
        if series.exists():
            self.stdout.write(self.style.SUCCESS("\nСериалы:"))
            for s in series:
                self.stdout.write(
                    f"  - {s.content.title}, Количество серий: {s.episodes_count}, Дата первого сезона: {s.first_season_date}")

