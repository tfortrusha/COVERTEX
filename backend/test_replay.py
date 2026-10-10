import time

from crypto.replay_protection import (
    generate_message_id,
    is_replay,
    is_timestamp_valid
)


# Simulate receiver's stored message IDs
received_ids = set()

# Create one message
message_id = generate_message_id()
timestamp = int(time.time())

print("Message ID:", message_id)
print("Timestamp valid:", is_timestamp_valid(timestamp))


# First reception
first_reception = is_replay(
    message_id,
    received_ids
)

print("First reception - Replay:", first_reception)


# Same message received again
second_reception = is_replay(
    message_id,
    received_ids
)

print("Second reception - Replay:", second_reception)