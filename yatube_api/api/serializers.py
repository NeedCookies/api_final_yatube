from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow, User


class AuthorSerializerMixin(serializers.Serializer):
    author = SlugRelatedField(slug_field='username', read_only=True)


class PostSerializer(AuthorSerializerMixin, serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(AuthorSerializerMixin, serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.Serializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message="Вы уже подписаны на этого пользователя."
            )
        ]

    def validate_following(self, value):
        """
        Проверка, что пользователь не подписывается сам на себя.
        """
        if self.context['request'].user == value:
            raise serializers.ValidationError("Нельзя подписаться на самого себя.")
        return value
