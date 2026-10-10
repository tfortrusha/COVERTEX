from crypto.image_payload import encrypt_image, decrypt_image
from crypto.key_utils import generate_key, generate_nonce
from crypto.steganography import embed_data, extract_data


INPUT_IMAGE = "carrier.png"
CARRIER_IMAGE = "carrier.png"
STEGO_IMAGE = "image_stego.png"
RECOVERED_IMAGE = "recovered_stego_image.png"


key = generate_key()
nonce = generate_nonce()


# 1. Encrypt image
ciphertext = encrypt_image(
    INPUT_IMAGE,
    key,
    nonce
)

print("Encrypted image size:", len(ciphertext), "bytes")


# 2. Embed encrypted image into carrier
embed_data(
    CARRIER_IMAGE,
    ciphertext,
    STEGO_IMAGE
)

print("Encrypted image embedded into:", STEGO_IMAGE)


# 3. Extract encrypted image
extracted_data = extract_data(STEGO_IMAGE)

print("Extracted data size:", len(extracted_data), "bytes")


# 4. Decrypt extracted image
decrypt_image(
    extracted_data,
    RECOVERED_IMAGE,
    key,
    nonce
)

print("Recovered image:", RECOVERED_IMAGE)