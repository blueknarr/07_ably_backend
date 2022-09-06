from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, user_name, name, phone_number, **extra_fields):
        if not email:
            raise ValueError(_('이메일을 입력해주세요.'))

        if not password:
            raise ValueError(_('비밀번호를 입력해주세요.'))

        if not user_name:
            raise ValueError(_('닉네임을 입력해주세요.'))

        if not name:
            raise ValueError(_('이름을 입력해주세요.'))

        if not phone_number:
            raise ValueError(_('전화번호를 입력해주세요.'))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            user_name=user_name,
            name=name,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, user_name, name, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, user_name, name, phone_number, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('이메일', max_length=100, unique=True)
    user_name = models.CharField('닉네임', max_length=50, unique=True)
    name = models.CharField('이름', max_length=20)
    phone_number = models.CharField('전화번호', max_length=11, unique=True)
    date_joined = models.DateTimeField('계정 생성일', auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'name', 'phone_number']

    objects = UserManager()

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.email
