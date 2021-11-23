from hmac import compare_digest


def safe_pwd_cmp(password1: str, password2: str):
    return bool(compare_digest(password1, password2))
