import time
import secrets


MAX_MESSAGE_AGE = 300  # 5 minutes


def generate_message_id() -> str:
    return secrets.token_hex(16)


def is_timestamp_valid(timestamp: int) -> bool:
    current_time = int(time.time())

    return abs(current_time - timestamp) <= MAX_MESSAGE_AGE


def is_replay(message_id: str, received_ids: set) -> bool:
    if message_id in received_ids:
        return True

    received_ids.add(message_id)

    return False