import re


def is_phone_number(num):
    """
    올바른 휴대폰 전화 번호인지 판별 (01012345678: True)
    :param num: String
    :return: Boolean
    """
    phone_regex = re.compile("^(010)\d{4}\d{4}")
    validation = phone_regex.search(num)

    if validation:
        return True
    return False


def password_validation_check(password):
    """
    비밀번호 정규표현식, 8자 이상 16자 이하, 소문자, 숫자 최소 하나 사용
    :param password: String
    :return: Boolean
    """
    password_regex = re.compile('^(?=.{8,16}$)(?=.*[a-z])(?=.*[0-9]).*$')
    validation = password_regex.search(password)

    if validation:
        return True
    return False
