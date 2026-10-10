from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def generate_signing_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    return private_key, public_key


def sign_message(private_key, message: bytes) -> bytes:
    return private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )


def verify_signature(public_key, message: bytes, signature: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception:
        return False


def save_public_key(public_key, file_path: str):
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(file_path, "wb") as file:
        file.write(public_bytes)


def load_public_key(file_path: str):
    with open(file_path, "rb") as file:
        return serialization.load_pem_public_key(file.read())