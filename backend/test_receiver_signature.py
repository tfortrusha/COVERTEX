from crypto.signatures import load_public_key, verify_signature
from crypto.message import parse_message
from crypto.steganography import extract_data

# Load the sender's public key
public_key = load_public_key("sender_public.pem")

# Extract the envelope from the received image
payload = extract_data("received_stego.png")
parsed = parse_message(payload)

# Reconstruct the signed data
ciphertext = bytes.fromhex(parsed["ciphertext"])
nonce = bytes.fromhex(parsed["nonce"])
timestamp = parsed["timestamp"]
message_id = parsed["message_id"]
signature = bytes.fromhex(parsed["signature"])

signed_data = (
    ciphertext
    + nonce
    + str(timestamp).encode()
    + message_id.encode()
)

# Verify the signature
valid = verify_signature(
    public_key,
    signed_data,
    signature
)

print("Message ID:", message_id)
print("Signature valid:", valid)