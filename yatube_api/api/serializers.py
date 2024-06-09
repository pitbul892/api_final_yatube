from django.core.exceptions import ValidationError
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Group, Follow, Post, User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post', )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def create(self, data):
        return Follow.objects.create(
            user=User.objects.get(username=data['user']),
            following=User.objects.get(username=data['following'])
        )

    def validate_following(self, data):
        user = self.context['request'].user
        following = data
        if following == user:
            raise ValidationError('Подписка на себя.')
        return super().validate(data)
