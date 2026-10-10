import asyncio
import pyshark

asyncio.set_event_loop(asyncio.new_event_loop())

capture = pyshark.LiveCapture(
    interface=r"\Device\NPF_{54FA002E-5C6A-4C59-BA83-69E924F5BFE2}",
    tshark_path=r"C:\Program Files\Wireshark\tshark.exe",
    output_file="covortex_capture.pcap"
)

print("Capturing 20 packets...")

count = 0

for packet in capture.sniff_continuously():
    try:
        print(
            packet.sniff_time,
            packet.highest_layer,
            packet.ip.src,
            "->",
            packet.ip.dst
        )

        count += 1

        if count >= 20:
            break

    except AttributeError:
        pass

capture.close()

print("Capture complete.")
print("Saved to: covortex_capture.pcap")