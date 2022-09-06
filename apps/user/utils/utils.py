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