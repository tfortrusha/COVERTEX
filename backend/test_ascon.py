from crypto.ascon_crypto import encrypt_message, decrypt_message
from crypto.key_utils import generate_key, generate_nonce


key = generate_key()
nonce = generate_nonce()

message = "Building B needs immediate assistance."

ciphertext = encrypt_message(message, key, nonce)

print("Original:", message)
print("Ciphertext:", ciphertext.hex())

decrypted = decrypt_message(ciphertext, key, nonce)

print("Decrypted:", decrypted)