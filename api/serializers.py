from rest_framework import serializers
from .models import UserProfile, Post


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model. Handles serialization of user profile data.
    """

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "email",
            "profile_picture",
            "short_description",
            "is_valid",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user. Includes custom create method
    for handling password encryption and optional fields.
    """

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "email",
            "password",
            "profile_picture",
            "short_description",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "profile_picture": {"required": False},
            "short_description": {"required": False},
        }

    def create(self, validated_data):
        """
        Custom create method to handle user creation with encrypted password.
        """
        user = UserProfile.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            profile_picture=(
                validated_data["profile_picture"]
                if "profile_picture" in validated_data
                else None
            ),
            short_description=validated_data["short_description"],
        )
        return user


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model. Includes nested user profile data for author
    and users who liked the post.
    """

    author = UserProfileSerializer(read_only=True)
    liked_by = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "updated_at",
            "liked_by",
            "is_deleted",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model, includes computed fields
    for total likes and total posts.
    """

    total_likes = serializers.SerializerMethodField()
    total_posts = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "profile_picture",
            "short_description",
            "total_likes",
            "total_posts",
        ]

    def get_total_likes(self, obj):
        """
        Returns the total number of posts liked by this user.
        """
        return obj.liked_posts.count()

    def get_total_posts(self, obj):
        """
        Returns the total number of posts created by this user.
        """
        return obj.posts.count()
