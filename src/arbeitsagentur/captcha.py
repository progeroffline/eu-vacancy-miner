import os
from twocaptcha import TwoCaptcha


def resolve_simple_captcha(filepath: str, two_captcha_api_key: str) -> str:
    solver = TwoCaptcha(two_captcha_api_key)
    result = solver.normal(filepath)
    os.remove(filepath)
    return result["code"]  # type: ignore
