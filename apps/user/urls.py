from django.urls import path
from .views import (
    Authentication,
    UserCreateViewSet
)

phone_auth = Authentication.as_view({
    "post": "auth"
})

register = UserCreateViewSet.as_view({
    "post": "register"
})

urlpatterns = [
    path("auth/", phone_auth, name="phone_auth"),
    path("register/", register, name="register"),
]