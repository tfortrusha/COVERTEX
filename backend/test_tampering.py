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
from crypto.replay_protection import generate_message_id
from crypto.message import create_message, parse_message


# =========================
# 1. KEY EXCHANGE
# =========================

private_a, public_a = generate_key_pair()
private_b, public_b = generate_key_pair()

secret_a = derive_shared_secret(private_a, public_b)
secret_b = derive_shared_secret(private_b, public_a)

key_a = derive_session_key(secret_a)
key_b = derive_session_key(secret_b)


# =========================
# 2. ENCRYPT
# =========================

message = "Building B needs immediate assistance."

nonce = generate_nonce()

ciphertext = encrypt_message(
    message,
    key_a,
    nonce
)


# =========================
# 3. SIGN
# =========================

timestamp = int(time.time())
message_id = generate_message_id()

signing_private, signing_public = generate_signing_key_pair()

signed_data = (
    ciphertext
    + nonce
    + str(timestamp).encode()
    + message_id.encode()
)

signature = sign_message(
    signing_private,
    signed_data
)


# =========================
# 4. CREATE ENVELOPE
# =========================

envelope = create_message(
    ciphertext,
    nonce,
    timestamp,
    message_id,
    signature
)


# =========================
# 5. PARSE ENVELOPE
# =========================

parsed = parse_message(envelope)

received_ciphertext = bytes.fromhex(
    parsed["ciphertext"]
)

received_nonce = bytes.fromhex(
    parsed["nonce"]
)

received_timestamp = parsed["timestamp"]

received_message_id = parsed["message_id"]

received_signature = bytes.fromhex(
    parsed["signature"]
)


# =========================
# 6. TAMPER WITH CIPHERTEXT
# =========================

tampered_ciphertext = bytearray(received_ciphertext)

tampered_ciphertext[0] ^= 1

tampered_ciphertext = bytes(tampered_ciphertext)


# =========================
# 7. VERIFY TAMPERED MESSAGE
# =========================

tampered_signed_data = (
    tampered_ciphertext
    + received_nonce
    + str(received_timestamp).encode()
    + received_message_id.encode()
)

signature_valid = verify_signature(
    signing_public,
    tampered_signed_data,
    received_signature
)

print("Original signature valid: True")
print("Tampered signature valid:", signature_valid)

if not signature_valid:
    print("Tampering detected: True")
else:
    print("Tampering detected: False")