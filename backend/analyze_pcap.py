import asyncio
import pyshark

asyncio.set_event_loop(asyncio.new_event_loop())

PCAP_FILE = "covortex_capture.pcap"

capture = pyshark.FileCapture(
    PCAP_FILE,
    tshark_path=r"C:\Program Files\Wireshark\tshark.exe"
)

print("Analyzing PCAP...\n")

count = 0

for packet in capture:
    try:
        timestamp = packet.sniff_time
        protocol = packet.highest_layer
        length = packet.length

        if hasattr(packet, "ip"):
            source = packet.ip.src
            destination = packet.ip.dst
        else:
            source = "N/A"
            destination = "N/A"

        print(
            f"{timestamp} | "
            f"{protocol} | "
            f"{source} -> {destination} | "
            f"Length: {length}"
        )

        count += 1

    except AttributeError:
        pass

capture.close()

print(f"\nTotal packets analyzed: {count}")