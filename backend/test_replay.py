from crypto.replay_protection import (
    generate_message_id,
    is_replay
)


received_ids = set()

message_id = generate_message_id()

print("Message ID:", message_id)


# First time receiving the message
print(
    "First reception:",
    is_replay(message_id, received_ids)
)


# Same message received again
print(
    "Second reception:",
    is_replay(message_id, received_ids)
)