from PIL import Image
import numpy as np


CARRIER = "carrier.png"
STEGO = "stego.png"


def lsb_ratio(image_path):
    image = np.array(
        Image.open(image_path).convert("RGB")
    )

    # Extract LSBs from all RGB channels
    lsbs = image & 1

    total = lsbs.size
    ones = np.sum(lsbs)

    return ones / total


carrier_ratio = lsb_ratio(CARRIER)
stego_ratio = lsb_ratio(STEGO)

print("===== BASIC STATISTICAL STEGANALYSIS =====")

print(f"Carrier LSB 1 ratio: {carrier_ratio:.6f}")
print(f"Stego LSB 1 ratio:   {stego_ratio:.6f}")

difference = abs(carrier_ratio - stego_ratio)

print(f"Difference:          {difference:.6f}")