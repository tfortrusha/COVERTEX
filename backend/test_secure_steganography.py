import time
from crypto.audit_log import initialize_database, log_event
from crypto.key_exchange import generate_key_pair, derive_shared_secret
from crypto.kdf import derive_session_key
from crypto.ascon_crypto import encrypt_message, decrypt_message
from crypto.key_utils import generate_nonce
from crypto.signatures import (
    generate_signing_key_pair,
    sign_message,
    verify_signature
)
from crypto.replay_protection import (
    generate_message_id,
    is_timestamp_valid,
    is_replay
)
from crypto.message import create_message, parse_message
from crypto.steganography import embed_data, extract_data

initialize_database()

SENDER = "Device_A"
RECEIVER = "Device_B"

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
# 2. ENCRYPT MESSAGE
# =========================

message = "Building B needs immediate assistance."

nonce = generate_nonce()

ciphertext = encrypt_message(
    message,
    key_a,
    nonce
)


# =========================
# 3. SIGN MESSAGE
# =========================

timestamp = int(time.time())
message_id = generate_message_id()

signing_private, signing_public = generate_signing_key_pair()
from crypto.signatures import save_public_key

save_public_key(signing_public, "sender_public.pem")
print("Sender public key saved.")

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
# 5. HIDE ENVELOPE IN IMAGE
# =========================

embed_data(
    "carrier.png",
    envelope,
    "stego.png"
)

print("Message hidden inside stego.png")


log_event(
    sender=SENDER,
    receiver=RECEIVER,
    event="MESSAGE_SENT",
    message_id=message_id,
    status="SUCCESS"
)

# =========================
# 6. EXTRACT FROM IMAGE
# =========================

extracted_data = extract_data("stego.png")

parsed = parse_message(extracted_data)

print("Envelope extracted successfully")

print("Extracted message ID:", parsed["message_id"])
print("Extracted timestamp:", parsed["timestamp"])
# =========================
# 7. READ EXTRACTED DATA
# =========================

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
# 8. SECURITY CHECKS
# =========================

timestamp_valid = is_timestamp_valid(
    received_timestamp
)

received_ids = set()

replay_detected = is_replay(
    received_message_id,
    received_ids
)

received_signed_data = (
    received_ciphertext
    + received_nonce
    + str(received_timestamp).encode()
    + received_message_id.encode()
)

signature_valid = verify_signature(
    signing_public,
    received_signed_data,
    received_signature
)

log_event(
    sender=SENDER,
    receiver=RECEIVER,
    event="SIGNATURE_VERIFICATION",
    message_id=message_id,
    status="SUCCESS" if signature_valid else "FAILED"
)

# =========================
# 9. DECRYPT
# =========================

if timestamp_valid and not replay_detected and signature_valid:

    decrypted = decrypt_message(
        received_ciphertext,
        key_b,
        received_nonce
    )

    print("Decrypted message:", decrypted)

else:
    print("Message rejected")


# =========================
# 10. RESULTS
# =========================

print()
print("Timestamp valid:", timestamp_valid)
print("Replay detected:", replay_detected)
print("Signature valid:", signature_valid)
print("Receiver signature check completed.")
print("Original message:", message)
print("Recovered message:", decrypted)
print("Messages match:", message == decrypted)