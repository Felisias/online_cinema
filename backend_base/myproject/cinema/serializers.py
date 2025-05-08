from rest_framework import serializers
from .models import (
    User,
    Genre,
    Content,
    Movie,
    Series,
    Season,
    Episode
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Content
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    content = ContentSerializer()

    class Meta:
        model = Movie
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    content = ContentSerializer()

    class Meta:
        model = Series
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    series = SeriesSerializer()

    class Meta:
        model = Season
        fields = '__all__'

class EpisodeSerializer(serializers.ModelSerializer):
    season = SeasonSerializer()

    class Meta:
        model = Episode
        fields = '__all__'
