from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from .models import User
from apps.post.models import Post, Comment

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    followers = UserDetailSerializer(many=True, read_only=True)
    following = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'total_posts', 'total_comments', 'followers', 'following']

    def get_total_posts(self, obj):
        return Post.objects.filter(author=obj).count()

    def get_total_comments(self, obj):
        return Comment.objects.filter(author=obj).count()

    def get_followers(self, obj):
        return UserDetailSerializer(obj.followers.all(), many=True).data

    def get_following(self, obj):
        return UserDetailSerializer(obj.following.all(), many=True).data
    
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        
        return value

  
class FollowUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    follow_id = serializers.IntegerField()

    def validate(self, data):
        user_id = data.get('user_id')
        follow_id = data.get('follow_id')

        if user_id == follow_id:
            raise serializers.ValidationError("User cannot follow themselves.")
        
        try:
            user = User.objects.get(id=user_id)
            user_to_follow = User.objects.get(id=follow_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User(s) not found.")

        if user_to_follow in user.following.all():
            raise serializers.ValidationError("Already following this user.")

        return data
