from crypto.steganography import embed_data, extract_data

message = b"Emergency team required at Building B"

embed_data(
    "carrier.png",
    message,
    "stego.png"
)

extracted = extract_data("stego.png")

print("Original :", message)
print("Extracted:", extracted)
print("Match    :", message == extracted)