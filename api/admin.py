from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import UserProfile, Post


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "is_valid",
        "date_joined",
        "last_login",
        "approve_button",
    ]
    list_filter = ["is_valid", "date_joined", "last_login"]
    search_fields = ["username", "email"]
    ordering = ["-date_joined"]
    actions = ["make_valid"]

    def make_valid(self, request, queryset):
        queryset.update(is_valid=True)

    make_valid.short_description = "Mark selected users as valid"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_valid=True)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter + ["is_staff", "is_superuser"]
        return self.list_filter

    def approve_button(self, obj):
        if obj.is_valid:
            return "Already Approved"
        else:
            url = reverse("admin:approve-user", args=[obj.pk])
            return format_html('<a class="button" href="{}">Approve</a>', url)

    approve_button.short_description = "Approve"

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:user_id>/approve/",
                self.admin_site.admin_view(self.approve_user),
                name="approve-user",
            ),
        ]
        return custom_urls + urls

    def approve_user(self, request, user_id):
        user = UserProfile.objects.get(pk=user_id)
        user.is_valid = True
        user.save()
        self.message_user(request, f"User {user.username} has been approved.")
        return HttpResponseRedirect("../")


class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "content", "created_at", "is_deleted"]
    list_filter = ["is_deleted", "created_at", "author"]
    search_fields = ["content", "author__username"]
    actions = ["restore_post"]

    def restore_post(self, request, queryset):
        for post in queryset:
            post.restore()

    restore_post.short_description = "Restore selected posts"


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post, PostAdmin)
