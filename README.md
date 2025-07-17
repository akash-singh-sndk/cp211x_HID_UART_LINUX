# CP2110 Linux SDK & Python HID UART Control

This repository provides tools and scripts for working with Silicon Labs CP2110 HID USB-to-UART bridge devices on Linux. It includes:

- A Bash setup script for SDK extraction, environment configuration, and device permissions
- A Python module for direct device control, diagnostics, and GPIO/UART management

---

## Prerequisite: Download the SDK

Before running the setup script, you must download the Silicon Labs USBXpress Host SDK for Linux:

**[Download USBXpressHostSDK-Linux.tar](https://www.silabs.com/documents/public/software/USBXpressHostSDK-Linux.tar)**

After downloading, place the `USBXpressHostSDK-Linux.tar` file in the parent directory of this repository so the setup script can find and extract it.

---
---

## 1. Bash Script: `setup_cp2110_linux.sh`

### Purpose
Automates the installation and environment setup for the Silicon Labs USBXpress Host SDK, ensuring all required libraries, Python modules, and device permissions are ready for development and testing.

### Main Features
- **SDK Extraction:** Unpacks the SDK archive into a local `sdk` directory
- **Architecture Detection:** Detects system architecture (x86_64, x86_32, ARM) and selects the correct library binaries
- **Library Linking:** Creates symbolic links in the working directory for the required `.so` shared libraries
- **Python Support:** Copies official Python support files if available
- **udev Rules:** Installs or provides instructions for udev rules to grant non-root access to CP2110 devices
- **Test Script Generation:** Creates a `test_cp2110.py` Python script for quick device enumeration and diagnostics
- **Environment Script:** Generates `setup_environment.sh` to set `PYTHONPATH` and `LD_LIBRARY_PATH` for development sessions

### Usage
```sh
bash setup_cp2110_linux.sh
source ./setup_environment.sh
python3 test_cp2110.py
```

---

## 2. Python Module: `cp211x_HID_UART.py`

### Purpose
Provides a Python interface to the CP2110 device using the Silicon Labs HID-to-UART API, enabling device enumeration, attribute reading, GPIO/UART control, and diagnostics.

### Main Features
- **Device Enumeration:** Lists all connected CP2110 devices, displaying VID, PID, and serial numbers
- **Attribute Access:** Reads device attributes, UART configuration, and GPIO latch states
- **GPIO Control:** Power on/off/cycle and print GPIO state with color-coded output
- **Error Handling:** Maps error codes to human-readable messages and raises exceptions for API errors
- **Class Abstraction:** `HidUartDevice` class wraps all device operations, making it easy to open, close, and interact with devices
- **Interactive CLI:** Allows users to select power operations and view live device diagnostics

### Example Output
```
================= HID Device Information =================
  Serial Number   : 0001
  Manufacturer    : Silicon Labs
  Product         : CP2110 HID USB-to-UART Bridge
  Part Number     : 10 (Version: 1)
  VID            : 0x10C4  PID: 0xEA80  Release: 0x0100
  UART Config     : baud=115200, dataBits=3, parity=0, stopBits=0, flowControl=0
  UART FIFO       : TX=0, RX=0
  UART Error Stat.: 0x00  Line Break Stat.: 0x00
  GPIO Latch      : 0xBFFF  [GPIO0=HIGH, GPIO1=HIGH, ...]
```

---

## 3. Workflow

1. **Setup:** Run the Bash script to extract the SDK, set up libraries, and configure the environment
2. **Development:** Source the environment script to ensure Python and system can find the required libraries
3. **Testing:** Use the provided Python module and scripts to enumerate and interact with CP2110 devices

---

## 4. Troubleshooting

- **Library Not Found:** Ensure symbolic links exist in the working directory and `LD_LIBRARY_PATH` is set
- **udev Permissions:** If you cannot access the device as a regular user, install the provided udev rules and reload them
- **Python Import Errors:** Make sure the Python script and libraries are in the same directory or in your `PYTHONPATH`

---

## 5. References

- [Silicon Labs CP2110 Documentation](https://www.silabs.com/documents/public/data-sheets/cp2110.pdf)
- [USBXpress Host SDK](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)

---

## License

See Silicon Labs End User License Agreement for SDK and driver usage.
