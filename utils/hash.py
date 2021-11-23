import hashlib


def hash_password(password: str) -> str:
    hashed_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_pwd
