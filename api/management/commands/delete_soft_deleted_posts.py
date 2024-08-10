# api/management/commands/delete_old_soft_deleted_posts.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from api.models import Post

class Command(BaseCommand):
    help = 'Hard delete posts that were soft deleted more than 10 days ago'

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=10)
        old_posts = Post.objects.filter(is_deleted=True, updated_at__lt=cutoff_date)
        count, _ = old_posts.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old soft-deleted posts'))
