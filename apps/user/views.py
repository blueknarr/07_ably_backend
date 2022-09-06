from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import (
    AuthenticationSerializer,
    RegisterSerializer,
    LoginSerializer
)


class Authentication(viewsets.GenericViewSet):
    """
    전화 번호 인증, 인증 제한 시간 180초
    010xxxxxxxx: 010 + 8자리 숫자
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
    my_auth_code: 전화번호 인증해서 받은 코드, "2435"
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
    식별 가능한 정보로 로그인 가능
    email: test@ably.com 또는
    user_name: test 또는
    phone_number: 01012345678
    """
    def get_serializer_class(self):
        return LoginSerializer

    @action(detail=False, methods=["post"])
    def login(self, request):
        login_serializer = self.get_serializer(data=request.data, context={"request": request})

        if login_serializer.is_valid(raise_exception=True):
            return Response(login_serializer.validated_data, status=status.HTTP_200_OK)
