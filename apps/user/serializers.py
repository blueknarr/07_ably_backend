import os

from .utils.utils import is_phone_number
from .models import User
from random import randint
from rest_framework import serializers
from dotenv import load_dotenv
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

load_dotenv()


class AuthenticationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, write_only=True)

    class Meta:
        model = User
        fields = ["phone_number"]

    def validate(self, attrs):
        if not is_phone_number(attrs["phone_number"]):
            raise serializers.ValidationError(_("유효하지 않은 휴대전화 번호입니다."))

        auth_code = str(randint(1000, 10000))
        cache.set(attrs["phone_number"], auth_code, int(os.environ["AUTH_CODE_TIMEOUT"]))
        data = {"인증 코드": auth_code}
        return data