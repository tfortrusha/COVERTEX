import time
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

from crypto.ascon_crypto import encrypt_message, decrypt_message


ITERATIONS = 100
MESSAGE_SIZES = [38, 64, 128]


# RSA key pair is generated once
rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
rsa_public_key = rsa_private_key.public_key()


for size in MESSAGE_SIZES:

    MESSAGE = "A" * size

    print(f"\n===== MESSAGE SIZE: {size} bytes =====")


    # ==================================================
    # ASCON
    # ==================================================

    ascon_key = os.urandom(16)
    ascon_nonce = os.urandom(16)

    ciphertext_ascon = encrypt_message(
        MESSAGE,
        ascon_key,
        ascon_nonce
    )

    start = time.perf_counter()

    for _ in range(ITERATIONS):
        encrypt_message(
            MESSAGE,
            ascon_key,
            os.urandom(16)
        )

    ascon_encrypt = time.perf_counter() - start


    start = time.perf_counter()

    for _ in range(ITERATIONS):
        decrypt_message(
            ciphertext_ascon,
            ascon_key,
            ascon_nonce
        )

    ascon_decrypt = time.perf_counter() - start


    # ==================================================
    # AES-GCM
    # ==================================================

    aes_key = AESGCM.generate_key(bit_length=128)
    aes = AESGCM(aes_key)
    aes_nonce = os.urandom(12)

    ciphertext_aes = aes.encrypt(
        aes_nonce,
        MESSAGE.encode(),
        None
    )

    start = time.perf_counter()

    for _ in range(ITERATIONS):
        aes.encrypt(
            os.urandom(12),
            MESSAGE.encode(),
            None
        )

    aes_encrypt = time.perf_counter() - start


    start = time.perf_counter()

    for _ in range(ITERATIONS):
        aes.decrypt(
            aes_nonce,
            ciphertext_aes,
            None
        )

    aes_decrypt = time.perf_counter() - start


    # ==================================================
    # RSA-2048
    # ==================================================

    ciphertext_rsa = rsa_public_key.encrypt(
        MESSAGE.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    start = time.perf_counter()

    for _ in range(ITERATIONS):
        rsa_public_key.encrypt(
            MESSAGE.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    rsa_encrypt = time.perf_counter() - start


    start = time.perf_counter()

    for _ in range(ITERATIONS):
        rsa_private_key.decrypt(
            ciphertext_rsa,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    rsa_decrypt = time.perf_counter() - start


    # ==================================================
    # RESULTS
    # ==================================================

    print(f"ASCON-128  : Encrypt {ascon_encrypt:.6f}s | Decrypt {ascon_decrypt:.6f}s")
    print(f"AES-GCM    : Encrypt {aes_encrypt:.6f}s | Decrypt {aes_decrypt:.6f}s")
    print(f"RSA-2048   : Encrypt {rsa_encrypt:.6f}s | Decrypt {rsa_decrypt:.6f}s")