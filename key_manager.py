import time
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class KeyManager:
    # Initialize a keyManager
    def __init__(self, key_ttl=60): # set keyttl with a lifespan of 60 seconds
        self.key_ttl = key_ttl
        self.keys = {}  # store keys with kid (unique id)
        self._generate_key() # generate key

    # Generate private and public key pair and assign with kid
    def _generate_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        kid = str(uuid.uuid4())
        expiry = time.time() + self.key_ttl # expiry time for key
        self.keys[kid] = {
            "private_key": private_key,
            "public_key": private_key.public_key(),
            "kid": kid,
            "expiry": expiry,
        }

    # GET a key and check to see expiration
    def get_key(self, expired=False):
        now = time.time()
        if expired:
            # If key is expired return its atributes 
            for key_data in self.keys.values():
                if key_data["expiry"] <= now:
                    return key_data
            # If the key does not exist, generate new one and set expiry time 
            self._generate_key()
            last_key = list(self.keys.values())[-1]
            last_key["expiry"] = now - 10  # expired 10 seconds ago
            return last_key
        else:
            # Return unexpired key
            for key_data in self.keys.values():
                if key_data["expiry"] > now:
                    return key_data
            # If none exist, generate a new one
            self._generate_key()
            return list(self.keys.values())[-1]

    # Return all unexpired keys based on expiry time
    def get_unexpired_keys(self):
        now = time.time()
        return {
            kid: key_data
            for kid, key_data in self.keys.items()
            if key_data["expiry"] > now
        }

    # Return jwks of all public unexpired keys 
    def get_public_jwks(self):
        keys = []
        for key_data in self.get_unexpired_keys().values():
            public_key = key_data["public_key"]
            public_numbers = public_key.public_numbers()
            e = public_numbers.e
            n = public_numbers.n

            # Have to convert to base64 url safe encoding
            e_b64 = self._int_to_base64(e)
            n_b64 = self._int_to_base64(n)

            jwk = {
                "kty": "RSA",   # key type
                "use": "sig", # needed for signature
                "alg": "RS256", # algorithm specification
                "kid": key_data["kid"], # key id
                "n": n_b64,
                "e": e_b64,
            }
            keys.append(jwk)

        return {"keys": keys}

    def _int_to_base64(self, val):
        # helper function to convert the enocding to base64, had to add this because RSA key components (jwks) 
        import base64

        b = val.to_bytes((val.bit_length() + 7) // 8, byteorder="big")
        return base64.urlsafe_b64encode(b).rstrip(b"=").decode("utf-8")
