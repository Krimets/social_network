from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'created_at', 'likes']
        read_only_fields = ['id', 'created_at', 'likes', 'user']
        extra_kwargs = {'text': {'required': True}}

    def get_user(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return UserSerializer(request.user).data
        return None

    def create(self, validated_data):
        user = self.context['request'].user
        post = Post.objects.create(user=user, **validated_data)
        return post


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    last_request = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'last_login', 'last_request']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CreatePostSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=240)

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        user = User.objects.get(id=user_id)
        post = Post.objects.create(user=user, **validated_data)
        return post

    def to_representation(self, instance):
        serializer = PostSerializer(instance, context=self.context)
        return serializer.data


class AnalyticsSerializer(serializers.Serializer):
    likes_by_date = serializers.DictField(child=serializers.IntegerField())

    def to_representation(self, instance):
        likes_by_date = {}
        for item in instance['likes_by_date']:
            likes_by_date[item['created_at'].timestamp()] = item['likes_count']
        return {'likes_by_date': likes_by_date}

