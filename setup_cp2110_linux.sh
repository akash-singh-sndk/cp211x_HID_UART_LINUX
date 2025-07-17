#!/bin/bash
# CP2110 Linux SDK Setup Script
# This script sets up the USBXpress Host SDK for Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SDK_ARCHIVE="USBXpressHostSDK-Linux/USBXpressHostSDK-6.7.7-Linux.tar.gz"
INSTALL_DIR="$SCRIPT_DIR/sdk"

echo "=========================================="
echo "CP2110 Linux SDK Setup"
echo "=========================================="

# Check if archive exists
if [ ! -f "$SCRIPT_DIR/$SDK_ARCHIVE" ]; then
    echo "Error: SDK archive not found at $SCRIPT_DIR/$SDK_ARCHIVE"
    echo "Please ensure the USBXpressHostSDK-6.7.7-Linux.tar.gz file is present."
    exit 1
fi

# Create installation directory
echo "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Extract SDK
echo "Extracting SDK archive..."
cd "$INSTALL_DIR"
tar -xzf "$SCRIPT_DIR/$SDK_ARCHIVE"

# Get system architecture
ARCH=$(uname -m)
case $ARCH in
    x86_64)
        LIB_ARCH="x86_64"
        ;;
    i686|i386)
        LIB_ARCH="x86_32"
        ;;
    armv7l|arm*)
        LIB_ARCH="arm7"
        ;;
    *)
        echo "Warning: Unsupported architecture $ARCH, defaulting to x86_64"
        LIB_ARCH="x86_64"
        ;;
esac

echo "Detected architecture: $ARCH -> Using libraries for: $LIB_ARCH"

# Set up library paths
CP2110_LIB_DIR="$INSTALL_DIR/USBXpressHostSDK/CP2110_4/lib/$LIB_ARCH"
CP2110_INCLUDE_DIR="$INSTALL_DIR/USBXpressHostSDK/CP2110_4/include"
CP2110_PYTHON_DIR="$INSTALL_DIR/USBXpressHostSDK/CP2110_4/python"

# Check if libraries exist
if [ ! -d "$CP2110_LIB_DIR" ]; then
    echo "Error: Library directory not found: $CP2110_LIB_DIR"
    exit 1
fi

# List available libraries
echo "Available libraries in $CP2110_LIB_DIR:"
ls -la "$CP2110_LIB_DIR"

# Create symbolic links for easier access
echo "Creating symbolic links..."
cd "$SCRIPT_DIR"

# Link libraries to current directory
ln -sf "$CP2110_LIB_DIR/libslabhiddevice.so.1.0" ./libslabhiddevice.so.1.0
ln -sf "$CP2110_LIB_DIR/libslabhidtouart.so.1.0" ./libslabhidtouart.so.1.0

# Also create version-less links
ln -sf "$CP2110_LIB_DIR/libslabhiddevice.so.1.0" ./libslabhiddevice.so
ln -sf "$CP2110_LIB_DIR/libslabhidtouart.so.1.0" ./libslabhidtouart.so

# Copy Python files if they exist
if [ -f "$CP2110_PYTHON_DIR/ComPortTestSuite.py" ]; then
    echo "Copying Python support files..."
    cp "$CP2110_PYTHON_DIR/ComPortTestSuite.py" ./
fi

if [ -f "$CP2110_LIB_DIR/SLABHIDtoUART.py" ]; then
    cp "$CP2110_LIB_DIR/SLABHIDtoUART.py" ./SLABHIDtoUART_official.py
fi

# Set up udev rules for device permissions (requires sudo)
UDEV_RULES_FILE="/etc/udev/rules.d/99-cp2110.rules"
if [ -f "$INSTALL_DIR/USBXpressHostSDK/CP2110_4/srcpkg/slabhiddevice/linux/SiliconLabs.rules" ]; then
    echo "Setting up udev rules for CP2110 devices..."
    if [ "$EUID" -eq 0 ]; then
        cp "$INSTALL_DIR/USBXpressHostSDK/CP2110_4/srcpkg/slabhiddevice/linux/SiliconLabs.rules" "$UDEV_RULES_FILE"
        udevadm control --reload-rules
        echo "Udev rules installed successfully."
    else
        echo "To set up device permissions, run the following commands as root:"
        echo "sudo cp '$INSTALL_DIR/USBXpressHostSDK/CP2110_4/srcpkg/slabhiddevice/linux/SiliconLabs.rules' '$UDEV_RULES_FILE'"
        echo "sudo udevadm control --reload-rules"
    fi
fi

# Create a simple test script
cat > test_cp2110.py << 'EOF'
#!/usr/bin/env python3
"""
Simple test script for CP2110 functionality
"""

try:
    from cp2110_linux_improved import *
    
    print("Testing CP2110 functionality...")
    print(f"Library version: {GetLibraryVersion()}")
    print(f"HID library version: {GetHidLibraryVersion()}")
    
    num_devices = GetNumDevices()
    print(f"Number of CP2110 devices found: {num_devices}")
    
    if num_devices > 0:
        print("Device details:")
        for i in range(num_devices):
            try:
                attrs = GetAttributes(i)
                serial = GetString(i)
                print(f"  Device {i}: VID=0x{attrs[0]:04X}, PID=0x{attrs[1]:04X}, Serial={serial}")
            except Exception as e:
                print(f"  Device {i}: Error - {e}")
    
    print("Test completed successfully!")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure the improved script is in the same directory.")
except Exception as e:
    print(f"Error: {e}")
EOF

chmod +x test_cp2110.py

# Create environment setup script
cat > setup_environment.sh << 'EOF'
#!/bin/bash
# Source this script to set up environment for CP2110 development

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Add current directory to Python path
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Add library directory to LD_LIBRARY_PATH
export LD_LIBRARY_PATH="$SCRIPT_DIR:$LD_LIBRARY_PATH"

echo "CP2110 development environment configured"
echo "Library path: $LD_LIBRARY_PATH"
echo "Python path: $PYTHONPATH"
EOF

chmod +x setup_environment.sh

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "Files created:"
echo "  - Library symbolic links in current directory"
echo "  - test_cp2110.py - Simple test script"
echo "  - setup_environment.sh - Environment setup"
echo ""
echo "To test the installation:"
echo "  1. Source the environment: source ./setup_environment.sh"
echo "  2. Run the test: python3 test_cp2110.py"
echo "  3. Or use the improved script: python3 cp2110_linux_improved.py --list"
echo ""
echo "Library architecture used: $LIB_ARCH"
echo "SDK installed in: $INSTALL_DIR"
