import secrets


def generate_key() -> bytes:
    """Generate a 128-bit ASCON key."""
    return secrets.token_bytes(16)


def generate_nonce() -> bytes:
    """Generate a 128-bit nonce."""
    return secrets.token_bytes(16)