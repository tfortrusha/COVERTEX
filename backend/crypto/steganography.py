from PIL import Image


def embed_data(image_path: str, data: bytes, output_path: str):
    image = Image.open(image_path).convert("RGB")

    pixels = list(image.getdata())

    # Convert bytes to bits
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    # Store the length of the data first (32 bits)
    data_length = len(data)
    length_bits = [
        (data_length >> i) & 1
        for i in range(31, -1, -1)
    ]

    all_bits = length_bits + bits

    if len(all_bits) > len(pixels) * 3:
        raise ValueError("Data is too large for this image")

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b = pixel

        channels = [r, g, b]

        for i in range(3):
            if bit_index < len(all_bits):
                channels[i] = (channels[i] & 0xFE) | all_bits[bit_index]
                bit_index += 1

        new_pixels.append(tuple(channels))

    stego_image = Image.new("RGB", image.size)
    stego_image.putdata(new_pixels)
    stego_image.save(output_path, "PNG")


def extract_data(image_path: str) -> bytes:
    image = Image.open(image_path).convert("RGB")

    pixels = list(image.getdata())

    bits = []

    for pixel in pixels:
        r, g, b = pixel

        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    # First 32 bits contain data length
    data_length = 0

    for bit in bits[:32]:
        data_length = (data_length << 1) | bit

    data_bits = bits[32:32 + data_length * 8]

    if len(data_bits) < data_length * 8:
        raise ValueError("Incomplete hidden data")

    data = bytearray()

    for i in range(0, len(data_bits), 8):
        byte = 0

        for bit in data_bits[i:i + 8]:
            byte = (byte << 1) | bit

        data.append(byte)

    return bytes(data)