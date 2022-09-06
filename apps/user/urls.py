from django.urls import path
from .views import (
    Authentication,
    UserCreateViewSet,
    UserLoginViewSet,
    UserLogoutViewSet,
    UserDetailViewSet,
    ChangePasswordViewSet
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

user_detail = UserDetailViewSet.as_view({
    "get": "retrieve"
})

change_password = ChangePasswordViewSet.as_view({
    "patch": "password"
})

urlpatterns = [
    path("auth/", phone_auth, name="phone_auth"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="login"),
    path("user/<int:user_id>/", user_detail, name="user_detail"),
    path("user/<int:user_id>/change-password/", change_password, name="change_password")
]