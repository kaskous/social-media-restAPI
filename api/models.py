from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    short_description = models.CharField(max_length=255, blank=True, null=True)
    is_valid = models.BooleanField(default=False)

    def get_total_likes(self):
        return self.liked_posts.count()

    def get_total_posts(self):
        return self.posts.count()


class Post(models.Model):
    author = models.ForeignKey(
        UserProfile, related_name="posts", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(
        UserProfile, related_name="liked_posts", blank=True
    )
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    @classmethod
    def delete_old_soft_deleted(cls):
        cutoff_date = timezone.now() - timedelta(days=10)
        cls.objects.filter(is_deleted=True, updated_at__lt=cutoff_date).delete()
