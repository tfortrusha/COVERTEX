from crypto.steganography import extract_data

payload = extract_data("received_stego.png")

print("Payload extracted successfully.")
print("Extracted payload size:", len(payload), "bytes")
print("First 20 bytes:", payload[:20].hex())