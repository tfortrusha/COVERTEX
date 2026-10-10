from crypto.image_payload import encrypt_image, decrypt_image
from crypto.key_utils import generate_key, generate_nonce


INPUT_IMAGE = "carrier.png"
OUTPUT_IMAGE = "recovered_image.png"


key = generate_key()
nonce = generate_nonce()


# Encrypt image
ciphertext = encrypt_image(
    INPUT_IMAGE,
    key,
    nonce
)

print("Original image size:", len(open(INPUT_IMAGE, "rb").read()), "bytes")
print("Encrypted data size:", len(ciphertext), "bytes")


# Decrypt image
decrypt_image(
    ciphertext,
    OUTPUT_IMAGE,
    key,
    nonce
)

print("Recovered image:", OUTPUT_IMAGE)