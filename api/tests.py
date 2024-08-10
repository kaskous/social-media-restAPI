from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UserProfile, Post


class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "testuser@example.com",
            "profile_picture": "",  # Set to empty string to avoid encoding None
            "short_description": "This is a test user",
        }
        self.user = UserProfile.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="testuser@example.com",
            short_description="This is a test user",
            is_valid=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_register_user(self):
        url = reverse("register")
        response = self.client.post(
            url,
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpassword123",
                "short_description": "This is a new user 2",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_login_user(self):
        url = reverse("login")
        response = self.client.post(
            url,
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "testpassword123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # JWT token should be returned

    def test_profile_retrieve(self):
        url = reverse("user-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["total_likes"], 0)
        self.assertEqual(response.data["total_posts"], 0)

    def test_profile_update(self):
        url = reverse("user-profile")
        response = self.client.patch(
            url,
            {
                "username": "newusername",
                "profile_picture": None,
                "short_description": "Updated description",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "newusername")
        self.assertEqual(response.data["short_description"], "Updated description")


class PostTests(APITestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="testuser@example.com",
            short_description="This is a test user",
            is_valid=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        url = reverse("post-list")
        post_data = {"content": "This is a test post"}
        response = self.client.post(url, post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().content, "This is a test post")

    def test_soft_delete_post(self):
        post = Post.objects.create(author=self.user, content="Post to be deleted")
        url = reverse("post-detail", args=[post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        post.refresh_from_db()
        self.assertTrue(post.is_deleted)

    def test_like_post(self):
        post = Post.objects.create(author=self.user, content="Post to be liked")
        url = reverse("post-like-post", args=[post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(post.liked_by.filter(id=self.user.id).exists())

    def test_unlike_post(self):
        post = Post.objects.create(author=self.user, content="Post to be unliked")
        post.liked_by.add(self.user)
        url = reverse("post-unlike-post", args=[post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(post.liked_by.filter(id=self.user.id).exists())
