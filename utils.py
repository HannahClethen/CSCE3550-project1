# This file was completed with assistance from Github Copilot

import time
import jwt
from cryptography.hazmat.primitives import serialization


def generate_jwt(private_key, kid, expiry=300):
    now = int(time.time())
    exp = now + expiry if expiry >= 0 else now + expiry  # allow negative expiry

    payload = {
        "sub": "fake_user",
        "iat": now,
        "exp": exp,
    }

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    token = jwt.encode(
        payload,
        key=pem,
        algorithm="RS256",
        headers={"kid": kid},
    )
    return token
