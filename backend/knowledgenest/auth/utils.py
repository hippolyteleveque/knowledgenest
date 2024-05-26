from bcrypt import hashpw, gensalt, checkpw


def create_hash(password: str):
    return hashpw(password.encode("utf-8"), gensalt())


def verify_hash(password, hashed_password):
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
