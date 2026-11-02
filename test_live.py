import asyncio
import json
import os
import sys
from bleak import BleakClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
HEART_RATE_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def hr_callback(sender, data):
    flags = data[0]
    hr_format = flags & 0x01
    bpm = data[1] if hr_format == 0 else ((data[2] << 8) | data[1])
    print(f"Heart Rate: {bpm} BPM")

async def main():
    config = load_config()
    if not config or "device_address" not in config:
        print("[ERROR] Configuration not found. Run 'main.py' to pair your device.")
        return

    device_address = config["device_address"]
    device_name = config.get("device_name", "Heart Rate Monitor")

    print(f"Connecting to {device_name} ({device_address})...")
    print("Press Ctrl+C to stop.")
    
    try:
        async with BleakClient(device_address) as client:
            if client.is_connected:
                # Добавили \n в конец этой строки
                print(f"Connected! Listening for heart rate data...\n") 
                await client.start_notify(HEART_RATE_MEASUREMENT_UUID, hr_callback)
                
                while client.is_connected:
                    await asyncio.sleep(1)
    except Exception as e:
        # Убрали \n из начала этой строки
        print(f"[ERROR] Connection lost or failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest stopped by user.")