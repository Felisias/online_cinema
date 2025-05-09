from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

#from django.contrib.auth.models import User

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('У пользователя должен быть email')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Хеширование пароля
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email





class Genre(models.Model):
    id = models.AutoField(primary_key=True)  # Уникальный ID (создаётся автоматически)
    name = models.CharField(max_length=255, unique=True)  # Название жанра

    def __str__(self):
        return self.name  # Удобное представление жанра в админке



class Content(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)  # Связь с жанром
    title = models.CharField(max_length=255)  # Название контента
    director = models.CharField(max_length=255, blank=True, null=True)  # Режиссёр
    age_rating = models.IntegerField()  # Возрастное ограничение

    def __str__(self):
        return self.title



class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)  # Связь 1:1 с контентом
    duration = models.IntegerField()  # Продолжительность в минутах
    release_date = models.DateField(blank=True, null=True)  # Дата выхода
    file_path = models.CharField(max_length=255, blank=True, null=True)  # Путь к файлу

    def __str__(self):
        return f"{self.content.title} (Movie)"



class Series(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)  # Связь 1:1 с контентом
    episodes_count = models.IntegerField()  # Общее число серий
    first_season_date = models.DateField(blank=True, null=True)  # Дата выхода первого сезона
    last_season_date = models.DateField(blank=True, null=True)  # Дата выхода последнего сезона

    def __str__(self):
        return f"{self.content.title} (Series)"



class Season(models.Model):
    id = models.AutoField(primary_key=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)  # Привязка к сериалу
    season_number = models.IntegerField()  # Номер сезона
    episodes_count = models.IntegerField()  # Число серий в сезоне
    release_date = models.DateField(blank=True, null=True)  # Дата выхода сезона

    def __str__(self):
        return f"Season {self.season_number} of {self.series.content.title}"



class Episode(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)  # Привязка к сезону
    title = models.CharField(max_length=255)  # Название эпизода
    duration = models.IntegerField()  # Длительность
    file_path = models.CharField(max_length=255, blank=True, null=True)  # Путь к файлу

    def __str__(self):
        return f"{self.title} (Episode of {self.season.series.content.title})"



class Review(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review for {self.content.title} — Rating: {self.rating}"
