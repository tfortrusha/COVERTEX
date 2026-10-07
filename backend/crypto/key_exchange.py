from cryptography.hazmat.primitives.asymmetric import ec


def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    return private_key, public_key


def derive_shared_secret(private_key, peer_public_key):
    return private_key.exchange(
        ec.ECDH(),
        peer_public_key
    )