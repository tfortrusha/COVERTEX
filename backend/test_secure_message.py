from crypto.key_exchange import generate_key_pair, derive_shared_secret
from crypto.kdf import derive_session_key
from crypto.ascon_crypto import encrypt_message, decrypt_message
from crypto.key_utils import generate_nonce


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


# Device B decrypts
decrypted = decrypt_message(
    ciphertext,
    key_b,
    nonce
)


print("Original:", message)
print("Ciphertext:", ciphertext.hex())
print("Decrypted:", decrypted)
print("Keys match:", key_a == key_b)