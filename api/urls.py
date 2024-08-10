from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LogoutView,
    RegisterView,
    UserProfileView,
    UserProfileViewSet,
    PostViewSet,
    FeedViewSet,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="userprofile")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"feed", FeedViewSet, basename="feed")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
