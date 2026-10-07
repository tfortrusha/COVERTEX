from crypto.key_utils import generate_key, generate_nonce


key = generate_key()
nonce = generate_nonce()

print("Key:", key.hex())
print("Key length:", len(key), "bytes")

print("Nonce:", nonce.hex())
print("Nonce length:", len(nonce), "bytes")