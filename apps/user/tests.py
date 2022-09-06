from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.exceptions import ErrorDetail


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        1. 슈퍼 유저 생성
        2. 일반 유저 생성
        3. 로그인 context
        """
        cls.c = Client()
        db = get_user_model()

        cls.super_user = db.objects.create_superuser(
            email="amdin@ably.com",
            password="admin1234",
            user_name="admin",
            name="admin",
            phone_number="01012345678"
        )

        cls.user = db.objects.create_user(
            email="test@ably.com",
            password="test1234",
            user_name="test",
            name="test",
            phone_number="01087654321"
        )

        cls.login_email_context = {
            "user_name": "test@ably.com",
            "password": "test1234"
        }
        cls.login_user_name_context = {
            "user_name": "test",
            "password": "test1234"
        }
        cls.login_phone_number_context = {
            "user_name": "01087654321",
            "password": "test1234"
        }

    def test_new_superuser(self):
        """
        관리자 계정 생성 TEST
        """
        self.assertEqual(self.super_user.email, "amdin@ably.com")
        self.assertEqual(self.super_user.user_name, "admin")
        self.assertEqual(self.super_user.name, "admin")
        self.assertEqual(self.super_user.phone_number, "01012345678")
        self.assertTrue(self.super_user.is_staff)
        self.assertTrue(self.super_user.is_superuser)
        self.assertTrue(self.super_user.is_active)

    def test_new_user(self):
        """
        일반 계정 생성 TEST
        """
        self.assertEqual(self.user.email, "test@ably.com")
        self.assertEqual(self.user.user_name, "test")
        self.assertEqual(self.user.name, "test")
        self.assertEqual(self.user.phone_number, "01087654321")
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)

    def test_get_auth_code(self):
        """
        전화번호 인증 TEST
        4자리 인증 코드 반환
        """
        response = self.c.post(
            "/api/v1/auth/",
            data={"phone_number": "01012341234"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_get_auth_code_error(self):
        """
        전화번호 인증 TEST
        010xxxxxxxx : 010 + 8자리 숫자만 허용
        """
        response = self.c.post(
            "/api/v1/auth/",
            data={"phone_number": "01112341234"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        """
        회원 가입 TEST
        전화번호 인증 후 회원 가입
        """
        response = self.c.post(
            "/api/v1/auth/",
            data={"phone_number": "01015881588"},
            content_type='application/json'
        )
        auth_code = response.data["인증 코드"]

        response= self.c.post(
            "/api/v1/register/",
            data={
                "email": "test2@ably.com",
                "password": "test1234",
                "user_name": "test2",
                "name": "test2",
                "phone_number": "01015881588",
                "my_auth_code": auth_code
            },
            content_type='application/json'
        )
        self.assertEqual(response.data, {"msg": "회원가입이 완료되었습니다."})
        self.assertEqual(response.status_code, 201)

    def test_register_error(self):
        """
        회원 가입 TEST
        전화번호 인증없이 회원 가입 진행
        """
        response= self.c.post(
            "/api/v1/register/",
            data={
                "email": "test2@ably.com",
                "password": "test1234",
                "user_name": "test2",
                "name": "test2",
                "phone_number": "01015881588",
            },
            content_type='application/json'
        )
        self.assertEqual(response.data, {'my_auth_code': [ErrorDetail(string='이 필드는 필수 항목입니다.', code='required')]})
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        """
        일반 계정 로그인 TEST
        식별 가능한 모든 정보로 로그인
        1. 이메일
        2. 닉네임
        3. 전화번호
        """
        response = self.c.post(
            "/api/v1/login/",
            data=self.login_email_context,
            content_type='application/json'
        )
        self.assertEqual(response.data, {"msg": f"{self.login_email_context['user_name']}님이 로그인하셨습니다."})
        self.assertEqual(response.status_code, 200)

        response = self.c.post(
            "/api/v1/login/",
            data=self.login_user_name_context,
            content_type='application/json'
        )
        self.assertEqual(response.data, {"msg": f"{self.login_user_name_context['user_name']}님이 로그인하셨습니다."})
        self.assertEqual(response.status_code, 200)

        response = self.c.post(
            "/api/v1/login/",
            data=self.login_phone_number_context,
            content_type='application/json'
        )
        self.assertEqual(response.data, {"msg": f"{self.login_phone_number_context['user_name']}님이 로그인하셨습니다."})
        self.assertEqual(response.status_code, 200)

    def test_login_error(self):
        """
        일반 계정 로그인 에러 TEST
        비밀번호 틀림
        """
        response = self.c.post(
            "/api/v1/login/",
            data={
                "user_name": "test@ably.com",
                "password": "test12"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_user_detail(self):
        """
        내 정보 보기 기능 TEST
        로그인 후 내 정보 보기 요청
        """
        response = self.c.post(
            "/api/v1/login/",
            data=self.login_email_context,
            content_type='application/json'
        )
        self.assertEqual(response.data, {"msg": f"{self.login_email_context['user_name']}님이 로그인하셨습니다."})
        self.assertEqual(response.status_code, 200)

        response = self.c.get(
            f"/api/v1/user/{self.user.id}/",
            content_type='application/json'
        )
        self.assertEqual(response.data, {'id': 2, 'email': 'test@ably.com', 'user_name': 'test', 'name': 'test', 'phone_number': '01087654321'})
        self.assertEqual(response.status_code, 200)

    def test_user_detail_error(self):
        """
        내 정보 보기 기능 TEST
        로그인을 하지 않고 내 정보 보기를 요청했을 때 에러
        """
        response = self.c.get(
            f"/api/v1/user/{self.user.id}/",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)

    def test_change_password(self):
        """
        로그인 없이 비밀번호 변경 TEST
        """
        response = self.c.post(
            "/api/v1/auth/",
            data={"phone_number": "01087654321"},
            content_type='application/json'
        )
        auth_code = response.data["인증 코드"]

        response = self.c.patch(
            f"/api/v1/user/{self.user.id}/change-password/",
            data={
                "phone_number": "01087654321",
                "password": "test5678",
                "my_auth_code": auth_code
            },
            content_type='application/json'
        )
        self.assertEqual(response.data, {"msg": f"{self.user.email}님의 비밀번호를 변경했습니다."})
        self.assertEqual(response.status_code, 200)

    def test_change_password_error(self):
        """
        로그인 없이 비밀번호 변경 TEST
        전화번호 인증 안함
        """
        response = self.c.patch(
            f"/api/v1/user/{self.user.id}/change-password/",
            data={
                "phone_number": "01015441544",
                "password": "test5678",
                "my_auth_code": "2345"
            },
            content_type='application/json'
        )
        self.assertEqual(response.data, [ErrorDetail(string='전화번호 인증이 필수입니다.', code='invalid')])
        self.assertEqual(response.status_code, 400)
