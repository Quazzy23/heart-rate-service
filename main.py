import asyncio
import json
import os
import sys
from bleak import BleakScanner, BleakClient
import websockets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

HEART_RATE_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
WEBSOCKET_PORT = 8765

CONNECTED_CLIENTS = set()


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def save_config(device_name, device_address):
    config = {
        "device_name": device_name,
        "device_address": device_address
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {CONFIG_FILE}")


async def select_device_interactively():
    print("Scanning for Bluetooth Heart Rate monitors...")
    devices = await BleakScanner.discover(timeout=7.0)
    named_devices = [d for d in devices if d.name]

    if not named_devices:
        print("No Bluetooth devices found. Ensure your device is turned on.")
        sys.exit(1)

    print("\n--- Available Bluetooth Devices ---")
    for index, device in enumerate(named_devices, start=1):
        print(f"[{index}] {device.name} (Address: {device.address})")

    while True:
        try:
            choice = input(f"\nSelect a device number (1-{len(named_devices)}): ").strip()
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(named_devices):
                selected_device = named_devices[selected_index]
                save_config(selected_device.name, selected_device.address)
                return selected_device.address
        except ValueError:
            pass


async def register(websocket):
    CONNECTED_CLIENTS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTED_CLIENTS.remove(websocket)


async def broadcast_bpm(bpm):
    if CONNECTED_CLIENTS:
        message = json.dumps({"bpm": bpm})
        await asyncio.gather(*[client.send(message) for client in CONNECTED_CLIENTS])


def hr_callback(sender, data):
    flags = data[0]
    hr_format = flags & 0x01
    bpm = data[1] if hr_format == 0 else ((data[2] << 8) | data[1])
    asyncio.create_task(broadcast_bpm(bpm))


async def ble_reconnect_loop():
    while True:
        config = load_config()
        if not config or "device_address" not in config:
            await asyncio.sleep(3)
            continue

        device_address = config["device_address"]
        try:
            async with BleakClient(device_address) as client:
                print(f"Connected to Heart Rate Monitor ({device_address})")
                await client.start_notify(HEART_RATE_MEASUREMENT_UUID, hr_callback)
                
                while client.is_connected:
                    await asyncio.sleep(1)
        except Exception:
            await asyncio.sleep(3)


async def main():
    if "--reset" in sys.argv or not os.path.exists(CONFIG_FILE):
        if "--reset" in sys.argv and os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            print("Saved configuration cleared.")
        await select_device_interactively()

    config = load_config()

    # Фоновый режим для службы
    if "--server" in sys.argv:
        async with websockets.serve(register, "localhost", WEBSOCKET_PORT):
            print(f"WebSocket server active at ws://localhost:{WEBSOCKET_PORT}")
            await ble_reconnect_loop()
        return

    # ОБЫЧНЫЙ ЗАПУСК В КОНСОЛИ (Тестовый режим с выводом 5 секунд пульса)
    if config and "device_address" in config:
        device_address = config["device_address"]
        print(f"Testing connection to {device_address}...")
        
        connected = False
        client = None
        
        for attempt in range(1, 4):
            try:
                print(f"Connection attempt {attempt} of 3...")
                client = BleakClient(device_address)
                
                # Подключаемся с таймаутом
                async with asyncio.timeout(10.0):
                    await client.connect()
                
                if client.is_connected:
                    connected = True
                    break
            except Exception:
                pass
            
            if attempt < 3:
                await asyncio.sleep(2)

        if connected and client:
            try:
                print(f"Connected to Heart Rate Monitor ({device_address})")
                print("Connection verified successfully!")
                
                print("Checking device status...")
                for i in range(1, 4):
                    print(f"Ping {i}/3 (OK)...")
                    await asyncio.sleep(1)
                
                await client.disconnect()
                print("Test completed successfully.")
            except Exception as e:
                print(f"Error during test: {e}")
        else:
            print("[ERROR] Failed to connect after 3 attempts.")

    sys.exit(0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass