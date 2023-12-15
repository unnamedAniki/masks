import jwt


def encode_token(secret: str, **payload) -> str:
    return jwt.encode(payload, secret, algorithm="HS256")