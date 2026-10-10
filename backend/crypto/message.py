import json


def create_message(
    ciphertext: bytes,
    nonce: bytes,
    timestamp: int,
    message_id: str,
    signature: bytes
) -> bytes:

    message = {
        "ciphertext": ciphertext.hex(),
        "nonce": nonce.hex(),
        "timestamp": timestamp,
        "message_id": message_id,
        "signature": signature.hex()
    }

    return json.dumps(message).encode("utf-8")


def parse_message(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))