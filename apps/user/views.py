
from .models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import AuthenticationSerializer


class Authentication(viewsets.GenericViewSet):
    """
    전화 번호 인증
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
