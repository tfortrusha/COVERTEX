import time

from crypto.key_exchange import generate_key_pair, derive_shared_secret
from crypto.kdf import derive_session_key
from crypto.ascon_crypto import encrypt_message
from crypto.key_utils import generate_nonce
from crypto.signatures import generate_signing_key_pair, sign_message
from crypto.message import create_message


# -------------------------
# 1. ECDH key exchange
# -------------------------

private_a, public_a = generate_key_pair()
private_b, public_b = generate_key_pair()

shared_secret = derive_shared_secret(private_a, public_b)
session_key = derive_session_key(shared_secret)


# -------------------------
# 2. Encrypt message
# -------------------------

message = "Building B needs immediate assistance."

nonce = generate_nonce()

ciphertext = encrypt_message(
    message,
    session_key,
    nonce
)


# -------------------------
# 3. Timestamp
# -------------------------

timestamp = int(time.time())


# -------------------------
# 4. Sign the encrypted data
# -------------------------

data_to_sign = (
    ciphertext
    + nonce
    + str(timestamp).encode()
)

signing_private, signing_public = generate_signing_key_pair()

signature = sign_message(
    signing_private,
    data_to_sign
)


# -------------------------
# 5. Create final envelope
# -------------------------

secure_message = create_message(
    ciphertext,
    nonce,
    timestamp,
    signature
)


print("Secure message:")
print(secure_message.decode())