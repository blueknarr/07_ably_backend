from django.urls import path
from .views import Authentication

phone_auth = Authentication.as_view({
    "post": "auth"
})

urlpatterns = [
    path("auth/", phone_auth, name="phone_auth")
]