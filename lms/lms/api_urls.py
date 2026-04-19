from django.urls import path, include


urlpatterns = [
    path("", include("apps.authz.urls")),
    path("", include("apps.library.urls")),
]
