from . import ascon


def encrypt_message(message: str, key: bytes, nonce: bytes) -> bytes:
    """
    Encrypt a message using Ascon-AEAD128.
    """

    associated_data = b"COVERTEX"

    ciphertext = ascon.ascon_encrypt(
        key,
        nonce,
        associated_data,
        message.encode("utf-8")
    )

    return ciphertext


def decrypt_message(ciphertext: bytes, key: bytes, nonce: bytes) -> str:
    """
    Decrypt and verify an Ascon-AEAD128 message.
    """

    associated_data = b"COVERTEX"

    plaintext = ascon.ascon_decrypt(
        key,
        nonce,
        associated_data,
        ciphertext
    )

    if plaintext is None:
        raise ValueError("Message authentication failed")

    return plaintext.decode("utf-8")