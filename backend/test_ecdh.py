from crypto.key_exchange import (
    generate_key_pair,
    derive_shared_secret
)


# Device A
private_a, public_a = generate_key_pair()

# Device B
private_b, public_b = generate_key_pair()


# Both devices derive the shared secret
secret_a = derive_shared_secret(private_a, public_b)
secret_b = derive_shared_secret(private_b, public_a)


print("Secret A:", secret_a.hex())
print("Secret B:", secret_b.hex())

print("Same secret:", secret_a == secret_b)