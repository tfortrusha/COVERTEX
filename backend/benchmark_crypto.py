import time
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

from crypto.ascon_crypto import encrypt_message, decrypt_message


MESSAGE_SIZES = [38, 64, 128]
ITERATIONS = 1000


# ==================================================
# ASCON-128
# ==================================================

ascon_key = os.urandom(16)
ascon_nonce = os.urandom(16)

# Encrypt once to obtain ciphertext
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

ascon_encrypt_time = time.perf_counter() - start


start = time.perf_counter()

for _ in range(ITERATIONS):
    decrypt_message(
        ciphertext_ascon,
        ascon_key,
        ascon_nonce
    )

ascon_decrypt_time = time.perf_counter() - start


# ==================================================
# AES-GCM
# ==================================================

aes_key = AESGCM.generate_key(bit_length=128)
aes = AESGCM(aes_key)

aes_nonce = os.urandom(12)

# Encrypt once to obtain ciphertext
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

aes_encrypt_time = time.perf_counter() - start


start = time.perf_counter()

for _ in range(ITERATIONS):
    aes.decrypt(
        aes_nonce,
        ciphertext_aes,
        None
    )

aes_decrypt_time = time.perf_counter() - start


# ==================================================
# RSA-2048
# ==================================================

rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

rsa_public_key = rsa_private_key.public_key()

# Encrypt once to obtain ciphertext
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

rsa_encrypt_time = time.perf_counter() - start


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

rsa_decrypt_time = time.perf_counter() - start


# ==================================================
# RESULTS
# ==================================================

print("\n===== COVERTEX CRYPTO BENCHMARK =====")
print(f"Iterations: {ITERATIONS}")
print(f"Message size: {len(MESSAGE.encode())} bytes\n")

print("ASCON-128")
print(f"  Encryption: {ascon_encrypt_time:.6f} seconds")
print(f"  Decryption: {ascon_decrypt_time:.6f} seconds")

print("\nAES-GCM")
print(f"  Encryption: {aes_encrypt_time:.6f} seconds")
print(f"  Decryption: {aes_decrypt_time:.6f} seconds")

print("\nRSA-2048")
print(f"  Encryption: {rsa_encrypt_time:.6f} seconds")
print(f"  Decryption: {rsa_decrypt_time:.6f} seconds")