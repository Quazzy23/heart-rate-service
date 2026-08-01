# 🫀 Local Bluetooth Heart Rate Overlay for OBS

**Local Heart Rate Overlay** is a lightweight, local, and lightning-fast heart rate monitor widget system designed for OBS Studio. Connect directly to any Bluetooth LE (BLE) heart rate monitor on your PC (such as **Coospo HW9**, **Polar H10**, **Garmin Dual**, **Magene**, and others) without relying on third-party cloud services, accounts, or VPNs.

---

## 🌟 Key Features

*   **100% Local & Private:** No third-party servers, accounts, or VPNs. Runs entirely on your machine.
*   **Zero Bloat:** Operates silently in the background via Windows Task Scheduler (no system tray icon, no startup tab clutter).
*   **Auto-Reconnect:** Automatically detects when your heart rate monitor wakes up and reconnects if the signal drops.
*   **Custom Overlays:** Fully customizable OBS widgets with dynamic color zones, real-time sync, and zero-latency WebSockets.
*   **Simple Management:** Easy 1-click batch files for setup, service installation, device switching, and uninstallation.

---

## 🚀 Installation & Setup Guide

### 1. Bluetooth Pairing in Windows
Turn on your heart rate monitor, open **Windows Bluetooth Settings**, and pair your device with your PC.

### 2. Configure the Device
Open your project terminal and run:
`python main.py`
Select your heart rate monitor from the detected list by entering its index number. A `config.json` file will be generated automatically, storing the device address.

### 3. Install the Background Service
Run **`install_service.bat`** to install dependencies and register the silent background task.
*   Verify execution via `taskschd.msc` (ensure `HeartRateService` state is **Running**).
*   *To pause the service, select "End" or "Disable".*

### 4. Previewing & Testing Widgets
The project includes ready-to-use HTML presets inside the `widgets/` folder, but you can also design your own custom overlays.
*   **Browser Preview:** Open any `.html` file inside the `widgets/` folder to inspect and test the visual style locally in your web browser.
*   **Adding to OBS:** Add a **Browser** source in OBS, check **Local file**, and point it to your preferred widget file.

### 5. Managing Devices & Uninstallation
*   **Switching Devices:** Run `Change-Device.bat` to safely terminate the background task, select a new monitor, update configuration, and resume operation.
*   **Full Removal:** Run **`uninstall_service.bat`** to completely clean up and remove the background task from Windows.

---

## 💡 Optional Debugging (Live Terminal Test)

Because Bluetooth LE permits only one active connection at a time, the live terminal test requires the background service to be inactive.
1. Open `taskschd.msc` and **End** the `HeartRateService` task.
2. Run the debugging script in your terminal:
   `python test_live.py`
3. Once finished, go back to `taskschd.msc` and **Run** the task back up.

---

## 👥 Authors & Credits

*   **Project Lead:** Quazzy ([@Quazzy23](https://github.com/Quazzy23))
*   **Development:** Created with the support of Google AI Gemini.

---
*Created with passion for clean code and seamless streaming tools.*