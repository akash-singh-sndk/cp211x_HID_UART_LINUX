#!/usr/bin/env python2
# Copyright (c) 2013-2015 by Silicon Laboratories Inc.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Silicon Laboratories End User
# License Agreement which accompanies this distribution, and is available at
# http://developer.silabs.com/legal/version/v10/License_Agreement_v10.htm
# Original content and implementation provided by Silicon Laboratories.

# ====================================== #
# Author:    Akash Kumar Singh           #
# Email:     akash.singh@sandisk.com     #
# ====================================== #


"""
Python wrapper for Silabs CP211x library (SLABHIDtoUART.dll).

Documentation for the library is provided by HID_to_UART_API_Specification.doc.
"""

import sys
# from ComPortTestSuite import *

import ctypes as ct

__version__ = "0.0.3"
__date__ = "02 September 2015"

__all__ = ['HID_UART', 'HID_UART_STATUS_DESC',
           'HidUartDevice', 'HidUartError', 'IsOpened',
           'GetNumDevices', 'GetAttributes', 'GetString',
           'GetLibraryVersion', 'GetHidLibraryVersion', "TestInvalDevIndex"]

# ==============================================================================

# Constants
# ==============================================================================


class HID_UART:
    VID = 0x10C4
    PID = 0xEA80

    VID_STR = 0x01
    PID_STR = 0x02
    PATH_STR = 0x03
    SERIAL_STR = 0x04
    MANUFACTURER_STR = 0x05
    PRODUCT_STR = 0x06

    FIVE_DATA_BITS = 0x00
    SIX_DATA_BITS = 0x01
    SEVEN_DATA_BITS = 0x02
    EIGHT_DATA_BITS = 0x03
    NO_PARITY = 0x00
    ODD_PARITY = 0x01
    EVEN_PARITY = 0x02
    MARK_PARITY = 0x03
    SPACE_PARITY = 0x04
    SHORT_STOP_BIT = 0x00
    LONG_STOP_BIT = 0x01
    NO_FLOW_CONTROL = 0x00
    RTS_CTS_FLOW_CONTROL = 0x01


# ==============================================================================
# Error Handling
# ==============================================================================

HID_UART_STATUS_DESC = {
    0x00: "HID_UART_SUCCESS",
    0x01: "HID_UART_DEVICE_NOT_FOUND",
    0x02: "HID_UART_INVALID_HANDLE",
    0x03: "HID_UART_INVALID_DEVICE_OBJECT",
    0x04: "HID_UART_INVALID_PARAMETER",
    0x05: "HID_UART_INVALID_REQUEST_LENGTH",
    0x10: "HID_UART_READ_ERROR",
    0x11: "HID_UART_WRITE_ERROR",
    0x12: "HID_UART_READ_TIMED_OUT",
    0x13: "HID_UART_WRITE_TIMED_OUT",
    0x14: "HID_UART_DEVICE_IO_FAILED",
    0x15: "HID_UART_DEVICE_ACCESS_ERROR",
    0x16: "HID_UART_DEVICE_NOT_SUPPORTED",
    0xFF: "HID_UART_UNKNOWN_ERROR",
}

# -------------------------------------------------------------------------------
# Constant definitions copied from the public DLL header
HID_UART_SUCCESS = 0x00
HID_UART_DEVICE_NOT_FOUND = 0x01
HID_UART_READ_TIMED_OUT = 0x12
HID_UART_WRITE_TIMED_OUT = 0x13

HID_UART_SHORT_STOP_BIT = 0
HID_UART_LONG_STOP_BIT = 1
HID_UART_NO_PARITY = 0
HID_UART_ODD_PARITY = 1
HID_UART_EVEN_PARITY = 2
HID_UART_MARK_PARITY = 3
HID_UART_SPACE_PARITY = 4
HID_UART_NO_FLOW_CONTROL = 0
HID_UART_RTS_CTS_FLOW_CONTROL = 1
HID_UART_FIVE_DATA_BITS = 0
HID_UART_SIX_DATA_BITS = 1
HID_UART_SEVEN_DATA_BITS = 2
HID_UART_EIGHT_DATA_BITS = 3


class HidUartError(Exception):
    def __init__(self, status):
        self.status = status
        try:
            self.name = HID_UART_STATUS_DESC[status]
        except:
            self.name = "HID_UART_STATUS_UNKNOWN: " + hex(status)

    def __str__(self):
        return self.name


def hiduart_errcheck(result, func, args):
    if result != HID_UART_SUCCESS:
        raise HidUartError(result)


# ==============================================================================
# CP211x HIDtoUART DLL
# ==============================================================================

if sys.platform == 'win32':
    _DLL = ct.windll.LoadLibrary("SLABHIDtoUART.dll")
elif sys.platform.startswith('linux'):
    _DLL_prev = ct.CDLL("./libslabhiddevice.so.1.0", mode=ct.RTLD_GLOBAL)
    _DLL = ct.cdll.LoadLibrary("./libslabhidtouart.so.1.0")
elif sys.platform == 'darwin':
    _DLL = ct.cdll.LoadLibrary("libSLABHIDtoUART.dylib")

# for win_function in ["HidUart_GetHidGuid",
    # "HidUart_GetIndexedString", "HidUart_GetOpenedIndexedString"]:
    # fnc = getattr(_DLL, win_function)
    # fnc.restype = ct.c_int
    # fnc.errcheck = hiduart_errcheck

for hiduart_function in ["HidUart_GetNumDevices",
                         "HidUart_GetAttributes", "HidUart_GetString",
                         "HidUart_GetLibraryVersion", "HidUart_GetHidLibraryVersion",
                         "HidUart_Open", "HidUart_Close",
                         "HidUart_IsOpened", "HidUart_GetPartNumber",
                         "HidUart_GetOpenedAttributes", "HidUart_GetOpenedString",
                         "HidUart_SetUartEnable", "HidUart_GetUartEnable",
                         "HidUart_FlushBuffers", "HidUart_CancelIo",
                         "HidUart_SetTimeouts", "HidUart_GetTimeouts",
                         "HidUart_SetUartConfig", "HidUart_GetUartConfig",
                         "HidUart_GetUartStatus", "HidUart_Reset",
                         "HidUart_StartBreak", "HidUart_StopBreak",
                         "HidUart_ReadLatch", "HidUart_WriteLatch"]:
    fnc = getattr(_DLL, hiduart_function)
    fnc.restype = ct.c_int
    fnc.errcheck = hiduart_errcheck

# Don't want hiduart_errcheck for these functions
getattr(_DLL, "HidUart_Read").restype = ct.c_int
getattr(_DLL, "HidUart_Write").restype = ct.c_int

# ==============================================================================
# Library Functions
# ==============================================================================
# Methods Not Implemented
#  HidUart_GetIndexedString(DWORD deviceNum, WORD vid, WORD pid, DWORD stringIndex, char* deviceString);
#  HidUart_GetHidGuid(void* guid);

# HidUart_GetNumDevices(DWORD* numDevices, WORD vid, WORD pid);


def GetNumDevices(vid=HID_UART.VID, pid=HID_UART.PID):
    """Returns the number of devices connected to the host with matching VID/PID."""
    ndev = ct.c_ulong()
    _DLL.HidUart_GetNumDevices(ct.byref(ndev), vid, pid)
    return ndev.value

# HidUart_GetAttributes(DWORD deviceNum, WORD vid, WORD pid, WORD* deviceVid, WORD* devicePid, WORD* deviceReleaseNumber);


def GetAttributes(index=0, vid=HID_UART.VID, pid=HID_UART.PID):
    """Returns VID, PID and release number for the indexed device with matching VID/PID."""
    dev_vid = ct.c_ushort()
    dev_pid = ct.c_ushort()
    dev_rel = ct.c_ushort()
    _DLL.HidUart_GetAttributes(index, vid, pid, ct.byref(
        dev_vid), ct.byref(dev_pid), ct.byref(dev_rel))
    return (dev_vid.value, dev_pid.value, dev_rel.value)

# HidUart_GetString(DWORD deviceNum, WORD vid, WORD pid, char* deviceString, DWORD options);


def GetString(index=0, vid=HID_UART.VID, pid=HID_UART.PID, opt=HID_UART.SERIAL_STR):
    """Returns the selected string for the indexed device with matching VID/PID."""
    buf = ct.create_string_buffer(512)
    _DLL.HidUart_GetString(index, vid, pid, buf, opt)
    return buf.value.decode()

# HidUart_GetLibraryVersion(BYTE* major, BYTE* minor, BOOL* release);


def GetLibraryVersion():
    """Returns the SLABHIDtoUART library version number as a string."""
    major = ct.c_byte()
    minor = ct.c_byte()
    release = ct.c_long()
    _DLL.HidUart_GetLibraryVersion(
        ct.byref(major), ct.byref(minor), ct.byref(release))
    return "{}.{}.{}".format(major.value, minor.value, release.value)

# HidUart_GetHidLibraryVersion(BYTE* major, BYTE* minor, BOOL* release);


def GetHidLibraryVersion():
    """Returns the SLABHIDDevice library version number as a string."""
    major = ct.c_byte()
    minor = ct.c_byte()
    release = ct.c_long()
    _DLL.HidUart_GetHidLibraryVersion(
        ct.byref(major), ct.byref(minor), ct.byref(release))
    return "{}.{}.{}".format(major.value, minor.value, release.value)


def IsOpened(index=0, vid=HID_UART.VID, pid=HID_UART.PID):
    """Checks if the indexed device with matching VID/PID is already open."""
    status = 0
    try:
        GetAttributes(index, vid, pid)
    except HidUartError as e:
        status = e.status
    # 0x15 : "HID_UART_DEVICE_ACCESS_ERROR"
    return bool(status == 0x15)


# ==============================================================================
# HidUart Class
# ==============================================================================
# Methods Not Implemented:
#  HidUart_GetOpenedIndexedString(HID_UART_DEVICE device, DWORD stringIndex, char* deviceString);
#
#  Device customization functions:
#  HidUart_SetLock(HID_UART_DEVICE device, WORD lock);
#  HidUart_GetLock(HID_UART_DEVICE device, WORD* lock);
#  HidUart_SetUsbConfig(HID_UART_DEVICE device, WORD vid, WORD pid, BYTE power, BYTE powerMode, WORD releaseVersion, BYTE flushBuffers, BYTE mask);
#  HidUart_GetUsbConfig(HID_UART_DEVICE device, WORD* vid, WORD* pid, BYTE* power, BYTE* powerMode, WORD* releaseVersion, BYTE* flushBuffers);
#  HidUart_SetManufacturingString(HID_UART_DEVICE device, char* manufacturingString, BYTE strlen);
#  HidUart_GetManufacturingString(HID_UART_DEVICE device, char* manufacturingString, BYTE* strlen);
#  HidUart_SetProductString(HID_UART_DEVICE device, char* productString, BYTE strlen);
#  HidUart_GetProductString(HID_UART_DEVICE device, char* productString, BYTE* strlen);
#  HidUart_SetSerialString(HID_UART_DEVICE device, char* serialString, BYTE strlen);
#  HidUart_GetSerialString(HID_UART_DEVICE device, char* serialString, BYTE* strlen);

class HidUartDevice(object):
    """
    HidUartDevice instances are used to work with a specific CP211x device.

    For help on the wrapped functions, refer to HID_to_UART_API_Specification.doc.
    """

    def __init__(self):
        self.handle = ct.c_void_p(0)

    # HidUart_Open(HID_UART_DEVICE* device, DWORD deviceNum, WORD vid, WORD pid);
    def Open(self, DevIndex, vid=HID_UART.VID, pid=HID_UART.PID):
        GetNumDevices()
        _DLL.HidUart_Open(ct.byref(self.handle), DevIndex, vid, pid)

    # HidUart_Close(HID_UART_DEVICE device);
    def Close(self):
        if self.handle.value:
            _DLL.HidUart_Close(self.handle)
            self.handle.value = 0

    # HidUart_IsOpened(HID_UART_DEVICE device, BOOL* opened);
    def IsOpened(self):
        opened = ct.c_long(0)
        if self.handle:
            _DLL.HidUart_IsOpened(self.handle, ct.byref(opened))
        return bool(opened.value)

    # HidUart_GetOpenedAttributes(HID_UART_DEVICE device, WORD* deviceVid, WORD* devicePid, WORD* deviceReleaseNumber);
    def GetAttributes(self):
        vid = ct.c_ushort(0)
        pid = ct.c_ushort(0)
        rel = ct.c_ushort(0)
        _DLL.HidUart_GetOpenedAttributes(
            self.handle, ct.byref(vid), ct.byref(pid), ct.byref(rel))
        return (vid.value, pid.value, rel.value)

    # HidUart_GetPartNumber(HID_UART_DEVICE device, BYTE* partNumber, BYTE* version);
    def GetPartNumber(self):
        pno = ct.c_byte(0)
        ver = ct.c_byte(0)
        _DLL.HidUart_GetPartNumber(self.handle, ct.byref(pno), ct.byref(ver))
        return (pno.value, ver.value)

    # HidUart_GetOpenedString(HID_UART_DEVICE device, char* deviceString, DWORD options);
    def GetString(self, opt=HID_UART.SERIAL_STR):
        buf = ct.create_string_buffer(512)
        _DLL.HidUart_GetOpenedString(self.handle, buf, opt)
        return buf.value.decode()

    # HidUart_SetUartEnable(HID_UART_DEVICE device, BOOL enable);
    def SetUartEnable(self, enable=True):
        _DLL.HidUart_SetUartEnable(self.handle, enable)

    # HidUart_GetUartEnable(HID_UART_DEVICE device, BOOL* enable);
    def GetUartEnable(self):
        enable = ct.c_long(0)
        _DLL.HidUart_GetUartEnable(self.handle, ct.byref(enable))
        return bool(enable.value)

    # HidUart_FlushBuffers(HID_UART_DEVICE device, BOOL flushTransmit, BOOL flushReceive);
    def FlushBuffers(self, flushTransmit=True, flushReceive=True):
        _DLL.HidUart_FlushBuffers(self.handle, flushTransmit, flushReceive)

    # HidUart_CancelIo(HID_UART_DEVICE device);
    def CancelIo(self):
        _DLL.HidUart_CancelIo(self.handle)

    # HidUart_Read(HID_UART_DEVICE device, BYTE* buffer, DWORD numBytesToRead, DWORD* numBytesRead);
    def Read(self, size=256):
        buf = ct.create_string_buffer(size)
        cnt = ct.c_ulong(0)
        status = _DLL.HidUart_Read(self.handle, buf, size, ct.byref(cnt))
        if status == HID_UART_SUCCESS or status == HID_UART_READ_TIMED_OUT:
            return buf.value
        else:
            raise

    def ReadString(self, size=256):
        return self.Read(size).decode('ascii', 'ignore')

    # HidUart_Write(HID_UART_DEVICE device, BYTE* buffer, DWORD numBytesToWrite, DWORD* numBytesWritten);
    def Write(self, buffer):
        cnt = ct.c_ulong(0)
        status = _DLL.HidUart_Write(
            self.handle, buffer, len(buffer), ct.byref(cnt))
        if status == HID_UART_SUCCESS or status == HID_UART_WRITE_TIMED_OUT:
            return cnt.value
        else:
            raise

    def WriteString(self, string):
        return self.Write(string.encode('ascii', 'ignore'))

    # HidUart_SetTimeouts(HID_UART_DEVICE device, DWORD readTimeout, DWORD writeTimeout);
    def SetTimeouts(self, rto=1000, wto=1000):
        _DLL.HidUart_SetTimeouts(self.handle, rto, wto)

    # HidUart_GetTimeouts(HID_UART_DEVICE device, DWORD* readTimeout, DWORD* writeTimeout);
    def GetTimeouts(self):
        rto = ct.c_ulong(0)
        wto = ct.c_ulong(0)
        _DLL.HidUart_GetTimeouts(self.handle, ct.byref(rto), ct.byref(wto))
        return (rto.value, wto.value)

    # HidUart_GetUartStatus(HID_UART_DEVICE device, WORD* transmitFifoSize, WORD* receiveFifoSize, BYTE* errorStatus, BYTE* lineBreakStatus);
    def GetUartStatus(self):
        tx_fifo = ct.c_ushort(0)
        rx_fifo = ct.c_ushort(0)
        err_stat = ct.c_byte(0)
        lbr_stat = ct.c_byte(0)
        _DLL.HidUart_GetUartStatus(self.handle, ct.byref(tx_fifo), ct.byref(
            rx_fifo), ct.byref(err_stat), ct.byref(lbr_stat))
        return (tx_fifo.value, rx_fifo.value, err_stat.value, lbr_stat.value)

    # HidUart_SetUartConfig(HID_UART_DEVICE device, DWORD baudRate, BYTE dataBits, BYTE parity, BYTE stopBits, BYTE flowControl);
    def SetUartConfig(self, baud=115200, data=HID_UART.EIGHT_DATA_BITS,
                      parity=HID_UART.NO_PARITY, stop=HID_UART.SHORT_STOP_BIT, flow=HID_UART.NO_FLOW_CONTROL):
        _DLL.HidUart_SetUartConfig(self.handle, baud, data, parity, stop, flow)

    # HidUart_GetUartConfig(HID_UART_DEVICE device, DWORD* baudRate, BYTE* dataBits, BYTE* parity, BYTE* stopBits, BYTE* flowControl);
    def GetUartConfig(self):
        baud = ct.c_ulong()
        data = ct.c_ulong()
        parity = ct.c_ulong()
        stop = ct.c_ulong()
        flow = ct.c_ulong()
        _DLL.HidUart_GetUartConfig(self.handle, ct.byref(baud),
                                   ct.byref(data), ct.byref(parity), ct.byref(stop), ct.byref(flow))
        return (baud.value, data.value, parity.value, stop.value, flow.value)

    # HidUart_StartBreak(HID_UART_DEVICE device, BYTE duration);
    def StartBreak(self, duration=0):
        _DLL.HidUart_StartBreak(self.handle, duration)

    # HidUart_StopBreak(HID_UART_DEVICE device);
    def StopBreak(self):
        _DLL.HidUart_StopBreak(self.handle)

    # HidUart_Reset(HID_UART_DEVICE device);
    def Reset(self):
        _DLL.HidUart_Reset(self.handle)
        _DLL.HidUart_Close(self.handle)
        self.handle.value = 0

    # HidUart_ReadLatch(HID_UART_DEVICE device, WORD* latchValue);
    def ReadLatch(self):
        latch = ct.c_ushort()
        _DLL.HidUart_ReadLatch(self.handle, ct.byref(latch))
        return latch.value

    # HidUart_WriteLatch(HID_UART_DEVICE device, WORD latchValue, WORD latchMask);
    def WriteLatch(self, latch, mask):
        _DLL.HidUart_WriteLatch(self.handle, latch, mask)

    # ----------------------------------------------------------
    # Following methods emulate CComPort class from TestSuite and are required by TestSuite.py # Opens port, setst timeouts and clears it for test
    def Connect(self, DevIndex, vid=HID_UART.VID, pid=HID_UART.PID):
        self.Open(DevIndex, vid, pid)
        self.SetComTimeout(1000)
        self.Purge()

    def Purge(self):
        _DLL.HidUart_FlushBuffers(self.handle, True, True)

    def Disconnect(self):
        self.Close()

    def Read(self, buf, bytesToRead):
        BytesRead = ct.c_ulong(0)
        status = _DLL.HidUart_Read(
            self.handle, buf, bytesToRead, ct.byref(BytesRead))
        if status == HID_UART_SUCCESS or status == HID_UART_READ_TIMED_OUT:
            return BytesRead.value
        else:
            return 0

    def Write(self, buf, bytesToWrite):
        BytesWritten = ct.c_ulong(0)
        status = _DLL.HidUart_Write(
            self.handle, buf, bytesToWrite, ct.byref(BytesWritten))
        if status == HID_UART_SUCCESS or status == HID_UART_WRITE_TIMED_OUT:
            return BytesWritten.value
        else:
            return 0

    def SetComTimeout(self, timeout):
        # Add 200 ms to timeout for command overhead
        _DLL.HidUart_SetTimeouts(self.handle, timeout + 200, timeout + 200)

    # Translates Windows COM API parameters (WinComApi.py) into HidUart parameters, then configures port
    # SetComConfig(DWORD baud = 115200, BYTE dataBits = 8, BYTE parity = NOPARITY, BYTE stopBits = ONESTOPBIT, BYTE flowControl = COM_NO_FLOW_CONTROL);
    def SetComConfig(self, baud, dataBits, parity, stopBits, flowControl):

        if dataBits < 5 or dataBits > 8:
            print("Invalid dataBits %x" % dataBits)
            return -1

        if dataBits == 5:
            dataBits = HID_UART_FIVE_DATA_BITS
        elif dataBits == 6:
            dataBits = HID_UART_SIX_DATA_BITS
        elif dataBits == 7:
            dataBits = HID_UART_SEVEN_DATA_BITS
        else:
            dataBits = HID_UART_EIGHT_DATA_BITS

        # All validation and mapping now handled above using HID_UART_* constants only
        self.SetUartConfig(baud, dataBits, parity, stopBits, flowControl)
        return 0


def PRINTV(*arg):
    print(*arg)
    pass


def TestInvalDevIndex(NumDevices):
    rc = 0
    try:
        hu = HidUartDevice()
        hu.Open(NumDevices)
        rc = -1
    except Exception as e:
        # Python 3: catch all exceptions, check for attribute 'status'
        if hasattr(e, 'status') and e.status != HID_UART_DEVICE_NOT_FOUND:
            print("TestInvalDevIndex: Unexpected error:", e, "-", hex(e.status))
            rc = -1
    finally:
        return rc


def PowerOff(hu):
    print(
        "\n\033[1;34m==================== Executing Power Off ====================\033[0m\n")
    if hu.WriteLatch(0, 4) != None:  # 0 is to put pin 3 as off
        print("Error Writing Latch ")
        return 1
    latch = hu.ReadLatch()
    # Print GPIO info after operation

    def decode_gpio_latch(latch):
        # Professional: GPIOx: ON (green) / OFF (red), no random colors
        return ', '.join([
            f"GPIO{n}: " + ("\033[32mON\033[0m" if (latch &
                            (1 << n)) else "\033[31mOFF\033[0m")
            for n in range(8)
        ])
    try:
        print(
            "\033[1;34m------------------- GPIO State After Power Off -------------------\033[0m")
        print(
            f"  \033[33mLatch state   :\033[0m \033[37m{latch} (0x{latch:016b})\033[0m")
        print(
            f"  \033[33mGPIO Latch    :\033[0m \033[37m0x{latch:04X}\033[0m  [ {decode_gpio_latch(latch)} ]")
        gpio3_state = (latch & 0x8)
        
        print(
            "\033[1;34m------------------------------------------------------------------\033[0m\n")
    except Exception as e:
        print(f"\033[91m[Info] Could not fetch GPIO info: {e}\033[0m")
    return 0


def PowerOn(hu):
    print(
        "\n\033[1;34m==================== Executing Power On =====================\033[0m\n")
    if hu.WriteLatch(4, 4) != None:  # 4 is to put pin 3 as on
        print("Error Writing Latch ")
        return 1
    latch = hu.ReadLatch()
    # Print GPIO info after operation

    def decode_gpio_latch(latch):
        return ', '.join([
            f"GPIO{n}: " + ("\033[32mON\033[0m" if (latch &
                            (1 << n)) else "\033[31mOFF\033[0m")
            for n in range(8)
        ])
    try:
        print(
            "\033[1;34m------------------- GPIO State After Power On --------------------\033[0m")
        print(
            f"  \033[33mLatch state   :\033[0m \033[37m{latch} (0x{latch:016b})\033[0m")
        print(
            f"  \033[33mGPIO Latch    :\033[0m \033[37m0x{latch:04X}\033[0m  [ {decode_gpio_latch(latch)} ]")
        gpio3_state = (latch & 0x8)
        
        print(
            "\033[1;34m------------------------------------------------------------------\033[0m\n")
    except Exception as e:
        print(f"\033[91m[Info] Could not fetch GPIO info: {e}\033[0m")
    return 0


def PowerCycle(hu):
    print(
        "\n\033[1;34m==================== Executing Power Cycle ===================\033[0m\n")
    if hu.WriteLatch(0, 4) != None:  # 0 is to put pin 3 as off
        print("\033[91mError Writing Latch while Power Off\033[0m")
        return 1
    latch = hu.ReadLatch()

    def decode_gpio_latch(latch):
        return ', '.join([
            f"GPIO{n}: " + ("\033[32mON\033[0m" if (latch &
                            (1 << n)) else "\033[31mOFF\033[0m")
            for n in range(8)
        ])
    try:
        print(
            "\033[1;34m---------------- GPIO State After Power Off (Cycle) ----------------\033[0m")
        print(
            f"  \033[33mLatch state   :\033[0m \033[37m{latch} (0x{latch:016b})\033[0m")
        print(
            f"  \033[33mGPIO Latch    :\033[0m \033[37m0x{latch:04X}\033[0m  [ {decode_gpio_latch(latch)} ]")
        gpio3_state = (latch & 0x8)
        
        print(
            "\033[1;34m-------------------------------------------------------------------\033[0m\n")
    except Exception as e:
        print(f"\033[91m[Info] Could not fetch GPIO info: {e}\033[0m")
    print(
        "\n\033[1;34m-------------------- Powering On (Cycle) ---------------------\033[0m\n")
    if hu.WriteLatch(4, 4) != None:  # 4 is to put pin 3 as on
        print("\033[91mError Writing Latch while Power On\033[0m")
        return 1
    latch = hu.ReadLatch()
    try:
        print(
            "\033[1;34m---------------- GPIO State After Power On (Cycle) -----------------\033[0m")
        print(
            f"  \033[33mLatch state   :\033[0m \033[37m{latch} (0x{latch:016b})\033[0m")
        print(
            f"  \033[33mGPIO Latch    :\033[0m \033[37m0x{latch:04X}\033[0m  [ {decode_gpio_latch(latch)} ]")
        gpio3_state = (latch & 0x8)
        
        print(
            "\033[1;34m-------------------------------------------------------------------\033[0m\n")
    except Exception as e:
        print(f"\033[91m[Info] Could not fetch GPIO info: {e}\033[0m")
    return 0


def print_hid_device_info(hu):
    def decode_gpio_latch(latch):
        # Returns a string with pin states for pins 0-7, values in green
        return ', '.join([
            f"GPIO{n}=" + ("\033[32mHIGH\033[0m" if (latch & (1<<n)) else "\033[32mLOW\033[0m")
            for n in range(8)
        ])

    try:
        print("\n\033[1;36m================= HID Device Information =================\033[0m")
        # Serial
        try:
            serial = hu.GetString(HID_UART.SERIAL_STR)
            print(f"  \033[1;37mSerial Number   :\033[0m \033[32m{serial}\033[0m")
        except Exception as e:
            print(f"  \033[1;37mSerial Number   :\033[0m <Error: {e}>")
        # Manufacturer
        try:
            manufacturer = hu.GetString(HID_UART.MANUFACTURER_STR)
            print(f"  \033[1;37mManufacturer    :\033[0m \033[32m{manufacturer}\033[0m")
        except Exception as e:
            print(f"  \033[1;37mManufacturer    :\033[0m <Error: {e}>")
        # Product
        try:
            product = hu.GetString(HID_UART.PRODUCT_STR)
            print(f"  \033[1;37mProduct         :\033[0m \033[32m{product}\033[0m")
        except Exception as e:
            print(f"  \033[1;37mProduct         :\033[0m <Error: {e}>")
        # Part number and version
        try:
            part, ver = hu.GetPartNumber()
            print(f"  \033[1;37mPart Number     :\033[0m \033[32m{part}\033[0m (Version: \033[32m{ver}\033[0m)")
        except Exception as e:
            print(f"  \033[1;37mPart Number     :\033[0m <Error: {e}>")
        # Attributes
        try:
            vid, pid, rel = hu.GetAttributes()
            print(f"  \033[1;37mVID            :\033[0m \033[32m0x{vid:04X}\033[0m  \033[1;37mPID:\033[0m \033[32m0x{pid:04X}\033[0m  \033[1;37mRelease:\033[0m \033[32m0x{rel:04X}\033[0m")
        except Exception as e:
            print(f"  \033[1;37mAttributes      :\033[0m <Error: {e}>")
        # UART config
        try:
            baud, data, parity, stop, flow = hu.GetUartConfig()
            print(f"  \033[1;37mUART Config     :\033[0m baud=\033[32m{baud}\033[0m, dataBits=\033[32m{data}\033[0m, parity=\033[32m{parity}\033[0m, stopBits=\033[32m{stop}\033[0m, flowControl=\033[32m{flow}\033[0m")
        except Exception as e:
            print(f"  \033[1;37mUART Config     :\033[0m <Error: {e}>")

        # Live UART status
        try:
            tx_fifo, rx_fifo, err_stat, lbr_stat = hu.GetUartStatus()
            print(f"  \033[1;37mUART FIFO       :\033[0m TX=\033[32m{tx_fifo}\033[0m, RX=\033[32m{rx_fifo}\033[0m")
            print(f"  \033[1;37mUART Error Stat.:\033[0m \033[32m0x{err_stat:02X}\033[0m  \033[1;37mLine Break Stat.:\033[0m \033[32m0x{lbr_stat:02X}\033[0m")
        except Exception as e:
            print(f"  \033[1;37mUART Status     :\033[0m <Error: {e}>")

        # GPIO latch state
        try:
            latch = hu.ReadLatch()
            print(f"  \033[1;37mGPIO Latch      :\033[0m \033[32m0x{latch:04X}\033[0m  [ {decode_gpio_latch(latch)} ]")
        except Exception as e:
            print(f"  \033[1;37mGPIO Latch      :\033[0m <Error: {e}>")

        print("\033[1;36m========================================================\033[0m\n")
    except Exception as e:
        print(f"\033[91mError printing HID device info: {e}\033[0m")


if __name__ == "__main__":
    import sys

    errorlevel = 1
    opened = False
    hu = HidUartDevice()

    ndx = 0
    if len(sys.argv) > 1:
        ndx = int(sys.argv[1])

    try:
        NumDevices = GetNumDevices()

        if TestInvalDevIndex(NumDevices) == 0:
            errorlevel = 0
            if NumDevices:
                hu.Open(ndx)
                print_hid_device_info(hu)
                prompt = (
                    "\n\033[1;36mPlease select an action:\033[0m\n"
                    "  \033[93m1\033[0m - \033[91mPower OFF\033[0m\n"
                    "  \033[93m2\033[0m - \033[92mPower ON\033[0m\n"
                    "  \033[93m3\033[0m - \033[94mPower Cycle\033[0m\n"
                    "\033[1;36mEnter your choice (1/2/3): \033[0m"
                )
                while True:
                    userinput = input(prompt).strip()
                    if userinput in ("1", "2", "3"):
                        userinput = int(userinput)
                        break
                    else:
                        print(
                            "\033[91mInvalid input. Please enter 1, 2, or 3.\033[0m")
                if userinput == 1:
                    errorlevel = PowerOff(hu)
                elif userinput == 2:
                    errorlevel = PowerOn(hu)
                elif userinput == 3:
                    errorlevel = PowerCycle(hu)

    except HidUartError as e:
        print("Device Error:", e, "-", hex(e.status))
    finally:
        if opened:
            hu.Close()
        if errorlevel:
            print(
                "\n\033[1;31m============================== FAIL =============================\033[0m\n")
        else:
            print(
                "\n\033[1;32m============================== PASS =============================\033[0m\n")
        sys.exit(errorlevel)
