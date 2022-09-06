from django.urls import path
from .views import (
    Authentication,
    UserCreateViewSet,
    UserLoginViewSet,
    UserLogoutViewSet
)

phone_auth = Authentication.as_view({
    "post": "auth"
})

register = UserCreateViewSet.as_view({
    "post": "register"
})

login = UserLoginViewSet.as_view({
    "post": "login"
})

logout = UserLogoutViewSet.as_view({
    "get": "logout"
})

urlpatterns = [
    path("auth/", phone_auth, name="phone_auth"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="login"),
]