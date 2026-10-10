from pathlib import Path

from .ascon import ascon_encrypt, ascon_decrypt


def encrypt_image(image_path: str, key: bytes, nonce: bytes) -> bytes:
    image_path = Path(image_path)

    image_data = image_path.read_bytes()

    associated_data = b"COVERTEX-IMAGE"

    return ascon_encrypt(
        key,
        nonce,
        associated_data,
        image_data
    )


def decrypt_image(
    ciphertext: bytes,
    output_path: str,
    key: bytes,
    nonce: bytes
):
    associated_data = b"COVERTEX-IMAGE"

    image_data = ascon_decrypt(
        key,
        nonce,
        associated_data,
        ciphertext
    )

    if image_data is None:
        raise ValueError("Image authentication failed")

    Path(output_path).write_bytes(image_data)