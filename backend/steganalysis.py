from PIL import Image
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


CARRIER = "carrier.png"
STEGO = "stego.png"


original = np.array(
    Image.open(CARRIER).convert("RGB")
)

stego = np.array(
    Image.open(STEGO).convert("RGB")
)


psnr = peak_signal_noise_ratio(
    original,
    stego,
    data_range=255
)

ssim = structural_similarity(
    original,
    stego,
    channel_axis=2,
    data_range=255
)


print("===== STEGANALYSIS / IMAGE QUALITY =====")
print(f"PSNR: {psnr:.4f} dB")
print(f"SSIM: {ssim:.6f}")