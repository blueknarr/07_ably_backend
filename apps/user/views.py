from .models import User
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from .serializers import (
    AuthenticationSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserLogoutSerializer,
    UserDetailSerializer,
    ChangePasswordSerializer,
)


class Authentication(viewsets.GenericViewSet):
    """
    전화 번호 인증
    1. 010xxxxxxxx: 010 + 8자리 숫자 / 인증 제한 시간 180초
    예) "phone_number" : "01012345678"
    """
    def get_serializer_class(self):
        return AuthenticationSerializer

    @action(detail=False, methods=["post"])
    def auth(self, request):
        auth_serializer = self.get_serializer(data=request.data)

        if auth_serializer.is_valid(raise_exception=True):
            return Response(auth_serializer.validated_data, status=status.HTTP_201_CREATED)


class UserCreateViewSet(viewsets.GenericViewSet):
    """
    회원 가입
    1. auth에서 인증코드 받기
    2. db에 sample data 저장 완료
    sample data - user_id: 1 / email: test@ably.com / user_name: test / phone_number: 01012345678 / passowrd: test1234
    my_auth_code - auth에서 인증 코드 받기, "2435"
    """
    def get_serializer_class(self):
        return RegisterSerializer

    @action(detail=False, methods=["post"])
    def register(self, request):
        register_serializer = self.get_serializer(data=request.data)

        if register_serializer.is_valid(raise_exception=True):
            register_serializer.save()
            return Response({
                "msg": "회원가입이 완료되었습니다."
            }, status=status.HTTP_201_CREATED)

        return Response({
            "msg": "회원가입을 실패했습니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(viewsets.GenericViewSet):
    """
    로그인
    1. 식별 가능한 정보로 로그인 가능
    2. 다른 정보로 로그인하려면 로그아웃 필수
    user_name - test@ably.com / test / 01012345678
    password - test1234
    """
    def get_serializer_class(self):
        return LoginSerializer

    @action(detail=False, methods=["post"])
    def login(self, request):
        login_serializer = self.get_serializer(data=request.data, context={"request": request})

        if login_serializer.is_valid(raise_exception=True):
            return Response(login_serializer.validated_data, status=status.HTTP_200_OK)


class UserLogoutViewSet(viewsets.GenericViewSet):
    """
    로그아웃
    1. Execute 버튼 누르면 로그아웃
    """
    def get_serializer_class(self):
        return UserLogoutSerializer

    @action(detail=False, methods=["get"])
    def logout(self, request):
        logout(request)

        return Response({
            "msg": "로그아웃했습니다."
        }, status=status.HTTP_200_OK)


class UserDetailViewSet(LoginRequiredMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    내 정보 보기 기능
    로그인 상태에서 요청해야함
    1. sample data로 로그인
    2. user_id로 내 정보 가져오기
    sample data - user_id: 1 / email: test@ably.com / user_name: test / phone_number: 01012345678 / passowrd: test1234
    """
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return UserDetailSerializer


class ChangePasswordViewSet(mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    비밀번호 변경
    로그인 없이 전화번호 인증으로 비번 변경
    1. auth에서 인증 코드 받기
    2. 변경할 비밀번호 / 전화번호 / 인증 코드 전송
    sample data - user_id: 1 / passowrd: test1234 / phone_number: 01012345678 / my_auth_code: auth_code
    """
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return ChangePasswordSerializer

    @action(detail=False, methods=["patch"])
    def password(self, request, user_id=None):
        user = self.get_object()
        change_password_serializer = self.get_serializer(
            instance=user, data=request.data, context={"my_auth_code":request.data["my_auth_code"]})

        if change_password_serializer.is_valid(raise_exception=True):
            change_password_serializer.save()
            return Response({
                "msg": f"{user.email}님의 비밀번호를 변경했습니다."
            }, status=status.HTTP_200_OK)

        return Response({
            "msg": "비밀번호 변경을 실패했습니다."
        }, status=status.HTTP_400_BAD_REQUEST)