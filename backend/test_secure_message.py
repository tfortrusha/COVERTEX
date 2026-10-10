from crypto.key_exchange import generate_key_pair, derive_shared_secret
from crypto.kdf import derive_session_key
from crypto.ascon_crypto import encrypt_message, decrypt_message
from crypto.key_utils import generate_nonce
from crypto.replay_protection import generate_message_id
from crypto.signatures import generate_signing_key_pair, sign_message
from crypto.message import create_message
import time
from crypto.replay_protection import is_timestamp_valid, is_replay
from crypto.signatures import verify_signature
from crypto.message import parse_message

# Device A
private_a, public_a = generate_key_pair()

# Device B
private_b, public_b = generate_key_pair()


# ECDH shared secret
secret_a = derive_shared_secret(private_a, public_b)
secret_b = derive_shared_secret(private_b, public_a)


# Derive ASCON session keys
key_a = derive_session_key(secret_a)
key_b = derive_session_key(secret_b)


# Generate nonce for this message
nonce = generate_nonce()


# Device A encrypts
message = "Building B needs immediate assistance."

ciphertext = encrypt_message(
    message,
    key_a,
    nonce
)

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

envelope = create_message(
    ciphertext,
    nonce,
    timestamp,
    message_id,
    signature
)

print("Message ID:", message_id)
print("Timestamp:", timestamp)
print("Signature:", signature.hex())
print("Envelope:", envelope.decode())


parsed = parse_message(envelope)

received_ciphertext = bytes.fromhex(parsed["ciphertext"])
received_nonce = bytes.fromhex(parsed["nonce"])
received_timestamp = parsed["timestamp"]
received_message_id = parsed["message_id"]
received_signature = bytes.fromhex(parsed["signature"])

received_ids = set()

print("Timestamp valid:", is_timestamp_valid(received_timestamp))
print(
    "Replay detected:",
    is_replay(received_message_id, received_ids)
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

print("Signature valid:", signature_valid)


if (
    is_timestamp_valid(received_timestamp)
    and not is_replay(received_message_id, set())
    and signature_valid
):
    decrypted = decrypt_message(
        received_ciphertext,
        key_b,
        received_nonce
    )

    print("Decrypted:", decrypted)
else:
    print("Message rejected")


print("Original:", message)
print("Ciphertext:", ciphertext.hex())
print("Decrypted:", decrypted)
print("Keys match:", key_a == key_b)