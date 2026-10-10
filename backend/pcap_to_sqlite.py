import asyncio
import sqlite3
import pyshark

asyncio.set_event_loop(asyncio.new_event_loop())

PCAP_FILE = "covortex_capture.pcap"
DB_FILE = "../data/covortex_traffic.db"

capture = pyshark.FileCapture(
    PCAP_FILE,
    tshark_path=r"C:\Program Files\Wireshark\tshark.exe"
)

# Create database
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS packets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    protocol TEXT,
    source_ip TEXT,
    destination_ip TEXT,
    packet_length INTEGER
)
""")

count = 0

for packet in capture:
    try:
        timestamp = str(packet.sniff_time)
        protocol = packet.highest_layer
        packet_length = int(packet.length)

        if hasattr(packet, "ip"):
            source_ip = packet.ip.src
            destination_ip = packet.ip.dst
        else:
            source_ip = "N/A"
            destination_ip = "N/A"

        cursor.execute("""
        INSERT INTO packets
        (timestamp, protocol, source_ip, destination_ip, packet_length)
        VALUES (?, ?, ?, ?, ?)
        """, (
            timestamp,
            protocol,
            source_ip,
            destination_ip,
            packet_length
        ))

        count += 1

    except AttributeError:
        pass

capture.close()
connection.commit()
connection.close()

print(f"Inserted {count} packets into SQLite.")
print(f"Database: {DB_FILE}")