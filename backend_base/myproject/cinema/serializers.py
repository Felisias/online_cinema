from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    User,
    Genre,
    Content,
    Movie,
    Series,
    Season,
    Episode,
    Review
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  # автоматически хэшируется
        )
        return user



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    #genre = GenreSerializer()
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Content
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    #content = ContentSerializer()    уходим от вложенного словаря к ожиданию id
    content = serializers.PrimaryKeyRelatedField(queryset=Content.objects.all())  #  вот это ключ

    class Meta:
        model = Movie
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    #content = ContentSerializer()
    content = serializers.PrimaryKeyRelatedField(queryset=Content.objects.all())

    class Meta:
        model = Series
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    #series = SeriesSerializer()
    series = serializers.PrimaryKeyRelatedField(queryset=Series.objects.all())

    class Meta:
        model = Season
        fields = '__all__'

class EpisodeSerializer(serializers.ModelSerializer):
    #season = SeasonSerializer()
    season = serializers.PrimaryKeyRelatedField(queryset=Season.objects.all())

    class Meta:
        model = Episode
        fields = '__all__'


#class ReviewSerializer(serializers.ModelSerializer):
#    content = serializers.PrimaryKeyRelatedField(queryset=Content.objects.all())
#
#    class Meta:
#        model = Review
#        fields = '__all__'



#class ReviewSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Review
#        fields = '__all__'
#
#    def to_internal_value(self, data):
#        # Если пользователь не админ, удаляем поле 'user' из входящих данных
#        if not self.context['request'].user.is_staff:
#            data = data.copy()
#            data.pop('user', None)
#        return super().to_internal_value(data)
#
#    def create(self, validated_data):
#        # Для всех: если 'user' не указан, то ставим request.user
#        if 'user' not in validated_data:
#            validated_data['user'] = self.context['request'].user
#        return super().create(validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']  # пользователь не указывается напрямую

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)






class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен.")
        return value