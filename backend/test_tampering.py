import time

from crypto.key_exchange import generate_key_pair, derive_shared_secret
from crypto.kdf import derive_session_key
from crypto.ascon_crypto import encrypt_message
from crypto.key_utils import generate_nonce
from crypto.signatures import (
    generate_signing_key_pair,
    sign_message,
    verify_signature
)


# ECDH
private_a, public_a = generate_key_pair()
private_b, public_b = generate_key_pair()

shared_secret = derive_shared_secret(private_a, public_b)
session_key = derive_session_key(shared_secret)


# Encrypt
message = "Building B needs immediate assistance."
nonce = generate_nonce()

ciphertext = encrypt_message(
    message,
    session_key,
    nonce
)


# Timestamp
timestamp = int(time.time())


# Signing keys
signing_private, signing_public = generate_signing_key_pair()


# Data being signed
data_to_sign = (
    ciphertext
    + nonce
    + str(timestamp).encode()
)


# Sign
signature = sign_message(
    signing_private,
    data_to_sign
)


# Original verification
valid = verify_signature(
    signing_public,
    data_to_sign,
    signature
)

print("Original signature valid:", valid)


# -------------------------
# Tamper with ciphertext
# -------------------------

tampered_ciphertext = bytearray(ciphertext)
tampered_ciphertext[0] ^= 1

tampered_data = (
    bytes(tampered_ciphertext)
    + nonce
    + str(timestamp).encode()
)


# Verify tampered message
tampered_valid = verify_signature(
    signing_public,
    tampered_data,
    signature
)

print("Tampered signature valid:", tampered_valid)