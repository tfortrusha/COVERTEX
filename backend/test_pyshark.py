import asyncio
import pyshark

asyncio.set_event_loop(asyncio.new_event_loop())

capture = pyshark.LiveCapture(
    interface=None,
    tshark_path=r"C:\Program Files\Wireshark\tshark.exe"
)

print("PyShark + TShark configured successfully.")