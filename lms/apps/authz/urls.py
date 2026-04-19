from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.authz.views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="login-tokens"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-tokens"),
]
