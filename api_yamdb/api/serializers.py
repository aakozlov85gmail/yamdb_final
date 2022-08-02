import random
import string

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers

from reviews.models import User, Category, Genre, Title, Review, Comment
from .utils import get_tokens_for_user


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author',
            'score', 'pub_date',
        )

    def validate(self, data):
        if Review.objects.filter(
                title=self.context['view'].kwargs['title_id'],
                author=self.context['request'].user
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставить два отзыва на одно произведение')
        return data

    def validate_score(self, value):
        if not (0 < value <= 10):
            raise serializers.ValidationError(
                'Недопустимое значение. Оценка должна быть от 1 до 10!'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text',
            'author', 'pub_date',
        )


class UserSelfRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя'
            )
        return value

    def create(self, validated_data):
        confirmation_code = ''.join(
            (random.choice(string.ascii_letters) for i in range(16))
        )
        send_mail(
            'Код подтверждения от сервиса yamdb',
            f'Ваш код подтверждения - {confirmation_code}',
            'admin@yamdb.com',
            [validated_data['email']],
        )

        user = User.objects.create(
            confirmation_code=confirmation_code,
            role='AUTH_USER', **validated_data
        )
        return user


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=16)
    token = serializers.SerializerMethodField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])

        if data['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError('неверный код подтверждения')

        return data

    def get_token(self, obj):
        user = User.objects.get(username=obj['username'])
        token = get_tokens_for_user(user)['access']
        return token


class UsersForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для данных о текущем пользователе."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = (
            'username',
            'email',
            'role'
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genre


class GenreField(serializers.SlugRelatedField):
    """Сериализатор для поля Genre."""

    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class CategoryField(serializers.SlugRelatedField):
    """Сериализатор для поля Category."""

    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    genre = GenreField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )
        filter_backends = (DjangoFilterBackend,)
        search_fields = ('genre',)

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']
