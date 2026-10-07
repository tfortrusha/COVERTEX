from crypto.signatures import (
    generate_signing_key_pair,
    sign_message,
    verify_signature
)


# Sender
private_key, public_key = generate_signing_key_pair()

message = b"Building B needs immediate assistance."

# Sign
signature = sign_message(private_key, message)

# Verify
valid = verify_signature(
    public_key,
    message,
    signature
)

print("Signature:", signature.hex())
print("Signature valid:", valid)


# Test tampering
tampered_message = b"Building B is safe."

valid_tampered = verify_signature(
    public_key,
    tampered_message,
    signature
)

print("Tampered message valid:", valid_tampered)