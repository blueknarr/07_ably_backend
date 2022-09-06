import os

from django.contrib.auth import authenticate, login
from .utils.utils import is_phone_number, password_validation_check
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


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, write_only=True)
    password = serializers.CharField(write_only=True)
    user_name = serializers.CharField(max_length=50, write_only=True)
    name = serializers.CharField(max_length=20, write_only=True)
    phone_number = serializers.CharField(max_length=11, write_only=True)
    my_auth_code = serializers.CharField(max_length=4, write_only=True)

    def email_validation_check(self, email):
        if not email:
            raise serializers.ValidationError(_("이메일을 입력해주세요."))

        get_email = User.objects.filter(email__iexact=email)
        if get_email.count() > 0:
            raise serializers.ValidationError(_("가입한 이메일 주소입니다."))
        return email

    def passowrd_validation_check(self, password):
        if not password_validation_check(password):
            raise serializers.ValidationError(_("8자리 이상 소문자, 숫자를 포함해 주세요."))
        return password

    def user_name_validation_check(self, user_name):
        if not user_name:
            raise serializers.ValidationError(_("닉네임을 입력해주세요."))

        get_user_name = User.objects.filter(user_name__iexact=user_name)
        if get_user_name.count() > 0:
            raise serializers.ValidationError(_("이미 등록되어 있는 닉네임입니다."))

        return user_name

    def name_validation_check(self, name):
        if not name:
            raise serializers.ValidationError(_("이름을 입력해 주세요."))
        return name

    def phone_number_validation_check(self, phone_number, my_auth_code):
        if not is_phone_number(phone_number):
            raise serializers.ValidationError(_("유효하지 않은 전화번호입니다."))

        get_phone_number = User.objects.filter(phone_number__iexact=phone_number)
        if get_phone_number.count() > 0:
            raise serializers.ValidationError(_("이미 등록되어 있는 전화번호입니다."))

        auth_code = cache.get(phone_number)
        if auth_code is None:
            raise serializers.ValidationError(_("전화번호 인증이 필수입니다."))

        if my_auth_code != auth_code:
            raise serializers.ValidationError(_("인증코드가 일치하지 않습니다."))

        return phone_number

    def validate(self, attrs):
        attrs["phone_number"] = self.phone_number_validation_check(attrs["phone_number"], attrs["my_auth_code"])
        attrs["email"] = self.email_validation_check((attrs["email"]))
        attrs["password"] = self.passowrd_validation_check(attrs["password"])
        attrs["user_name"] = self.user_name_validation_check(attrs["user_name"])
        attrs["name"] = self.name_validation_check(attrs["name"])

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            user_name=validated_data["user_name"],
            name=validated_data["name"],
            phone_number=validated_data["phone_number"]
        )

        return user


class LoginSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["user_name", "password"]

    def validate(self, attrs):
        user = authenticate(self.context.get("request"), username=attrs["user_name"], password=attrs["password"])

        if user is None:
            raise serializers.ValidationError(_("아이디 또는 비밀번호를 확인해주세요."))

        login(self.context.get("request"), user)
        data = {
            "msg": f"{attrs['user_name']}님이 로그인하셨습니다."
        }
        return data


class UserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_name",]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "user_name",
            "name",
            "phone_number"
        ]