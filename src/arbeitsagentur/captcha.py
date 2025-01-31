import os
import time
from twocaptcha import TwoCaptcha


def resolve_simple_captcha(filepath: str, two_captcha_api_key: str) -> str:
    solver = TwoCaptcha(two_captcha_api_key)
    try:
        result = solver.normal(filepath)
    except Exception as e:
        print(e)
        time.sleep(3)
        return resolve_simple_captcha(filepath, two_captcha_api_key)

    os.remove(filepath)
    return result["code"].replace("\u0430", "")  # type: ignore
