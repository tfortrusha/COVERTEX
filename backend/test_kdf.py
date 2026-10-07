from crypto.key_exchange import generate_key_pair, derive_shared_secret
from crypto.kdf import derive_session_key


# Device A
private_a, public_a = generate_key_pair()

# Device B
private_b, public_b = generate_key_pair()


# ECDH
secret_a = derive_shared_secret(private_a, public_b)
secret_b = derive_shared_secret(private_b, public_a)


# Convert shared secret into ASCON key
key_a = derive_session_key(secret_a)
key_b = derive_session_key(secret_b)


print("Session Key A:", key_a.hex())
print("Session Key B:", key_b.hex())
print("Same key:", key_a == key_b)
print("Key length:", len(key_a))