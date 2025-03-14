from django.contrib import admin
from .models import Genre, Content, Movie, Series, Season, Episode

# Register your models here.

admin.site.register(Genre)
admin.site.register(Content)
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Season)
admin.site.register(Episode)
