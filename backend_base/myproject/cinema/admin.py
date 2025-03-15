from django.contrib import admin
from .models import Genre, Content, Movie, Series, Season, Episode
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

#from .models import Post
# Register your models here.

admin.site.register(Genre)
admin.site.register(Content)
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Season)
admin.site.register(Episode)
#admin.site.register(Post)
admin.site.register(User)

admin.site.register(User, UserAdmin)