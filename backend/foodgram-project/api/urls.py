from django.urls import include, path
from rest_framework import routers

# from .views import ()

app_name = "api"

router = routers.DefaultRouter()
# router.register("auth", AuthViewSet, basename="auth")
# router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
]
