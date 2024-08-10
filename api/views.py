from rest_framework import views, status, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import UserProfile, Post
from .permissions import IsValidUser
from .serializers import UserProfileSerializer, PostSerializer, UserRegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class RegisterView(views.APIView):
    """
    Handles user registration. The user is created but marked inactive until validated by a superuser.
    """

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_valid = False  # User must be validated by superuser
            user.save()
            return Response(
                UserRegisterSerializer(user).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    """
    Handles user logout by blacklisting the token (if applicable).
    """

    def post(self, request, *args, **kwargs):
        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles. Allows retrieval and updating of profiles.
    Non-superusers can only view and update their own profiles.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsValidUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        """
        Overrides the update method to prevent changes to email and password via this endpoint.
        """
        instance = self.get_object()
        if "email" in request.data or "password" in request.data:
            return Response(
                {"error": "Cannot update email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts. Supports creating, retrieving, updating, and
    soft-deleting posts. Also includes actions for liking and unliking posts.
    """

    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsValidUser]

    def perform_create(self, serializer):
        """
        Automatically set the author of the post to the current user.
        """
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete the post instead of permanently deleting it.
        """
        post = self.get_object()
        post.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def like_post(self, request, pk=None):
        """
        Custom action to like a post.
        """
        post = self.get_object()
        post.liked_by.add(request.user)
        post.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unlike_post(self, request, pk=None):
        """
        Custom action to unlike a post.
        """
        post = self.get_object()
        post.liked_by.remove(request.user)
        post.save()
        return Response(status=status.HTTP_200_OK)


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for displaying a feed of recent posts, ordered by creation date.
    Limited to the 20 most recent posts.
    """

    queryset = Post.objects.filter(is_deleted=False).order_by("-created_at")[:20]
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsValidUser]

    def list(self, request, *args, **kwargs):
        """
        Lists posts with pagination support if necessary.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the current user's profile.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsValidUser]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_valid:
            raise AuthenticationFailed("User account is not valid.")
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
