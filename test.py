# SmarterSoft - Reverse Engineered SmartFade Control Software
# Copyright (C) 2023 Diesel Thomas

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import struct
import usb.core
import usb.util
import time

# ETC Smartfade 1248 (0x14d5:0x0200):
#   Configuration 1:
#       Interface 1 (HID):
#           Endpoint 1 (Device Out, Host In):
#
#           Endpoint 2 (Device In, Host Out):
#
#       Interface 2 (Vendor):
#           bInterfaceClass: 255
#           Endpoint 3 (Device Out, Host In):
#               bmAttributes:
#                   Transfer Type: Bulk
#           Endpoint 4 (Device In, Host Out):
#               bmAttributes:
#                   Transfer Type: Bulk

# Endpoint 3 Data: (Host receiving)
# Standard 12 byte messages:
# 0400 0000 0000 0000 0000 0000 (Response to new events request if there are no new events)
#
# XXXX - 2 byte, little-endian, some sort of packet sequence number.
#      XXXX - 2 byte, little-endian, next packet size (zero if there is not another packet).


# Endpoint 4 Data: (Host transmitting)
# Standard 12 byte message:
# 0000 0000 0000 0000 0000 0000 (Ask for new events)
# 0100 0700 0000 0000 0000 0000 (Prepare to send another packet with a size described in bytes 2 and 3)
# 0000 0700 0000 0000 0000 0000
# XXXX - 2 byte, little-endian, some sort of packet sequence number. Does not seem to do anything
#      XXXX - 2 byte, little-endian, next packet size (zero if there is not another packet).

# Find our device
dev = usb.core.find(idVendor=0x14d5, idProduct=0x0200)

# Was it found?
if dev is None:
    raise ValueError('Smartfade not found')

# Detatch all interfaces from any kernel drivers
for cfg in dev:
    for intf in cfg:
        print(f"Checking interface {intf.bInterfaceNumber}")
        if dev.is_kernel_driver_active(intf.bInterfaceNumber):
            try:
                print(f"Detatching kernel driver from interface {intf.bInterfaceNumber}")
                dev.detach_kernel_driver(intf.bInterfaceNumber)
                usb.util.claim_interface(dev, intf.bInterfaceNumber)
            except usb.core.USBError as e:
                raise OSError(f"Could not detatch kernel driver from interface {intf.bInterfaceNumber}: {str(e)}")

# Function to release the device and reattach the device to the OS kernel
def cleanup():
    for intf in cfg:
        if not dev.is_kernel_driver_active(intf.bInterfaceNumber):
            usb.util.release_interface(dev, intf.bInterfaceNumber)

# Takes multiple strings with hex numbers
# Returns them as bytes
def hexStr2bString(*args):
    return bytes.fromhex(' '.join(args))

# Takes multiple ints
# Returns them as bytes
# def int2bString(*args, formatCode='B'):
def int2bString(*args):
    # return struct.pack(f"!{len(args)}{formatCode}", *args)
    return bytes(*args)

# Takes an array of bytes extracts indexes 2 and 3
# and interprets them as a little-endian number
def extractSize(bArray):
    return struct.unpack('<H', bArray[2:4])[0]

# Reset the usb interface to a known state
# dev.reset()

# Set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

cfg = dev.get_active_configuration() # Get active configuration
vendor_intf = usb.util.find_descriptor(cfg, bInterfaceClass=255) # Find data interface

assert vendor_intf is not None

vendor_endpoint_in = usb.util.find_descriptor(vendor_intf, bEndpointAddress=0x83) # Device to Host (EP3)
vendor_endpoint_out = usb.util.find_descriptor(vendor_intf, bEndpointAddress=0x04) # Host to Device (EP4)

assert vendor_endpoint_in is not None
assert vendor_endpoint_out is not None

# print("Ready")
# input("Press Enter to continue...")

# while True:
#     vendor_endpoint_out.write(hexStr2bString("0000 0000 0000 0000 0000 0000"))
#
#     # 0400 0000 0000 0000 0000 0000 (Normal)
#     ref = vendor_endpoint_in.read(12)
#     print(ref)
#     if extractSize(ref) > 0:
#         print(vendor_endpoint_in.read(extractSize(ref)))
#
#     time.sleep(0.5)


def readData(readCmd):
    vendor_endpoint_out.write(hexStr2bString(readCmd)) # Send our read command

    # 0400 0000 0000 0000 0000 0000 (Normal)
    ref = vendor_endpoint_in.read(12) # Expect to receive 12 bytes of data
    print(ref)
    if extractSize(ref) > 0: # If there is additional data listed also receive it
        print(vendor_endpoint_in.read(extractSize(ref)))


def sendCommand(cmdString):
    bString = hexStr2bString(cmdString)
    vendor_endpoint_out.write(hexStr2bString("0100") + struct.pack('<H', len(bString)) + hexStr2bString("0000 0000 0000 0000"))
    vendor_endpoint_out.write(bString)

def stateTest(cmdString, exclusions=[]):
    for i in range(0, 256):
        if i in exclusions:
            continue
        # print(cmdString + ' {:02x}'.format(i))
        sendCommand(cmdString + ' {:02x}'.format(i))

# if True:
    # vendor_endpoint_out.write(hexStr2bString("0100 0700 0000 0000 0000 0000"))
    # vendor_endpoint_out.write(hexStr2bString("0203 0014 0147 01")) # ind1 toggle
    # vendor_endpoint_out.write(hexStr2bString("0303 0014 0147 00")) # ind1 save?

    # vendor_endpoint_out.write(hexStr2bString("0203 0014 0147 01")) # ind1 on
    # vendor_endpoint_out.write(hexStr2bString("0303 0014 0147 00")) # ind1?

    # vendor_endpoint_out.write(hexStr2bString("0403 0014 0147 01")) # ind1 off
    # vendor_endpoint_out.write(hexStr2bString("0503 0014 0147 00")) # ind1?

    # vendor_endpoint_out.write(hexStr2bString("0203 0014 0134 01")) # blackout toggle?
    # vendor_endpoint_out.write(hexStr2bString("0303 0014 0134 00")) # blackout save?


    # vendor_endpoint_out.write(hexStr2bString("0003 0027 0900 00"))
    # vendor_endpoint_out.write(hexStr2bString("0103 0027 0700 00"))
    # vendor_endpoint_out.write(hexStr2bString("0000 0014 0147 01"))

    # readData("0000 0000 0000 0000 0000 0000")

    # Stuff yet to figure out
    # Patching
    # Output/input monitoring
    # IND button mode, affected by master, level
    # Seq edit

    # Memory manipulation
    # ???? ????
    #           XX memory page [00-0b]
    #             XX memory [00-17]
    #                ??
    #                  XX length of faders to change [01-30] (defaults to 30)
    #                     XX fader 1 level
    #                       XX fader 2 level...
    #                                                                                                                                          XX fader 48
    # Name is after 0306, refer to Fader descriptions for format
    # 0000 0000 0000 0000 ffff 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0306 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

    # 075a 0000 0000 0130 ff00 0000 ffff ffff ffff ffff 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0306 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
    # 045a 0000 000b 0130 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 007f 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0306 00 7400 6500 7300 7400 3100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 00

    # Fader descriptions
    # Text:               t    e    s    t    1         t    e    s    t    2         t    e    s    t    3
    # 1927 0009 0003 0600 7400 6500 7300 7400 3100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 00
    # 1a27 0009 0003 0600 7400 6500 7300 7400 3100 0000 7400 6500 7300 7400 3200 0000 0000 0000 0000 0000 0000 00
    # 1b27 0009 0003 0600 7400 6500 7300 7400 3100 0000 7400 6500 7300 7400 3200 0000 7400 6500 7300 7400 3300 00
    # Fader text: (MAX 6 chars per line for 3 lines)
    #           XX fader number
    #                  XX XX UTF-16 big endian (start of line 1)...
    #                                                XX XX UTF-16 big endian (start of line 2)...
    #                                                                              XX XX UTF-16 big endian (start of line 3)...
    # 0000 0009 0003 0600 4800 6500 6c00 6c00 6f00 0000 5700 6f00 7200 6c00 6400 0000 0000 0000 0000 0000 0000 00


    # Settings/Info

    # 0103 0027 0700 00 # ?? allowed chars? file name?
    # 0003 0027 0900 00 # ?? firmware version

    # Erase     XX
    # 0603 0027 0b00 00 # Memories
    # 0703 0027 0c00 00 # Sequences
    # 0803 0027 0d00 00 # Stack
    # 0503 0027 1000 00 # All

    # Button Intensity (Does not update until you go to settings)
    #             XX
    # 0213 0029 0004 5a3c 0103 0000 0001 7f00 0100 3200 3200 00 # 4 (min)
    # 0313 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # 100 (default) (max)
    # Display Brightness (Does not update until you go to settings)
    #                XX
    # 0213 0029 0064 043c 0103 0000 0001 7f00 0100 3200 3200 00 # 4 (min)
    # 0213 0029 0064 5a3c 0103 0000 0001 7f00 0100 3200 3200 00 # 90 (default)
    # 0313 0029 0064 643c 0003 0000 0001 7f00 0100 3200 3200 00 # 100  (max)
    # Display Contrast (Does not update until you go to settings)
    #                  XX
    # 0213 0029 0064 5a?? 0103 0000 0001 7f00 0100 3200 3200 00 # ? (min)
    # 0213 0029 0064 5a3c 0103 0000 0001 7f00 0100 3200 3200 00 # 60 (default)
    # 0313 0029 0064 5a5a 0003 0000 0001 7f00 0100 3200 3200 00 # 90  (max)
    # Crossfader          XX
    # 0213 0029 0064 5a3c 0103 0000 0001 7f00 0100 3200 3200 00 # Both ways
    # 0313 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # Upwards only (default)
    # DMX Speed             XX
    # 0b13 0029 0064 5a3c 0000 0000 0001 7f00 0100 3200 3200 00 # Slow
    # 0c13 0029 0064 5a3c 0001 0000 0001 7f00 0100 3200 3200 00 # Medium
    # 0d13 0029 0064 5a3c 0002 0000 0001 7f00 0100 3200 3200 00 # Fast
    # 0e13 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # Maximum (default)
    # DMX Input                XX
    # 1113 0029 0064 5a3c 0003 0100 0001 7f00 0100 3200 3200 00 # On Fader 01/01
    # 1213 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # Merge with output (default)
    # DMX Backup                 XX
    # 1313 0029 0064 5a3c 0003 0001 0001 7f00 0100 3200 3200 00 # Bump = Enable
    # 1413 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # Bump = Flash (default)
    # MIDI Channel                  XX
    # 1713 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # 1 (default)
    # 1813 0029 0064 5a3c 0003 0000 0101 7f00 0100 3200 3200 00 # 2
    # 1613 0029 0064 5a3c 0003 0000 0f01 7f00 0100 3200 3200 00 # 16 (max)
    # MIDI (music) on                 XX
    # 1913 0029 0064 5a3c 0003 0000 0000 7f00 0100 3200 3200 00 # off
    # 1a13 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # on (default)
    # MIDI MSC id                        XX
    # 2113 0029 0064 5a3c 0003 0000 0001 0000 0100 3200 3200 00 # 0
    # 2213 0029 0064 5a3c 0003 0000 0001 0100 0100 3200 3200 00 # 1
    # 2313 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # 127 (default) (max)
    # MIDI MSC on                          XX
    # 2613 0029 0064 5a3c 0003 0000 0001 7f01 0100 3200 3200 00 # on
    # 2713 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # off (default)
    # Up fade                                   XX XX
    # 2813 0029 0064 5a3c 0003 0000 0001 7f00 0100 0000 3200 00 # 0
    # 0413 0029 0064 5a3c 0003 0000 0001 7f00 0100 0100 3200 00 # 0.1
    # 2913 0029 0064 5a3c 0003 0000 0001 7f00 0100 0a00 3200 00 # 1
    # 0313 0029 0064 5a3c 0003 0000 0001 7f00 0100 0b00 3200 00 # 1.1
    # 2a13 0029 0064 5a3c 0003 0000 0001 7f00 0100 3200 3200 00 # 5 (default)
    # 0813 0029 0064 5a3c 0003 0000 0001 7f00 0102 4e00 3200 00 # 28:15
    # 0e13 0029 0064 5a3c 0003 0000 0001 7f00 01ff ff00 3200 00 # 109:13.6 (max)
    # Down fade (Same as up)                         XX XX
    # Wait (Same as up)                                   XX XX


    # 0203 0014 0000 [00-ff] # fader 1 intensity
    # 0203 0014 0017 [00-ff] # fader 24 intensity

    # 0203 0014 0030 [00-ff] # blackout fader
    # 0203 0014 0031 [00-ff] # bump fader
    # 0203 0014 0032 [00-ff] # crossfader A position
    # 0203 0014 0033 [00-ff] # crossfader B position

    # 0203 0014 0100 00 # bump 1 off
    # 0203 0014 0100 [01-ff] # bump 1 on
    # 0203 0014 0117 00 # bump 24 off
    # 0203 0014 0117 [01-ff] # bump 24 on



    # 0203 0014 0130 00 # rate toggle / release rate
    # 0203 0014 0130 01 # press rate
    # 0203 0014 0131 01 # crossfader play
    # 0203 0014 0132 00 # crossfader pause
    # 0203 0014 0133 01 # solo toggle
    # 0203 0014 0134 01 # blackout toggle
    # 0203 0014 0135 01 # preview (nop)
    # 0203 0014 0136 01 # 1-24
    # 0203 0014 0137 01 # 25-48
    # 0203 0014 0138 00 # release clear
    # 0203 0014 0138 01 # press clear
    # 0203 0014 0139 00 # release mems
    # 0203 0014 0139 01 # press mems
    # 0203 0014 013a 01 # next toggle
    # 0203 0014 013b 00 # stack toggle
    # 6003 0014 013c 01 # power/mode (nop)
    # 0203 0014 013d 01 # undo
    # 0203 0014 013e 01 # copy
    # 0203 0014 013f 01 # rec seq toggle
    # 0203 0014 0140 01 # magic
    # 0203 0014 0141 01 # rec mem toggle
    # 0203 0014 0142 01 # edit mem toggle
    # 0203 0014 0143 01 # snapshot
    # 0203 0014 0144 01 # exit
    # 0203 0014 0145 01 # back
    # 0203 0014 0146 01 # menu
    # 0203 0014 0147 01 # ind1 toggle
    # 0203 0014 0148 01 # ind2 toggle
    # 0203 0014 0149 01 # Scroll right
    # 0203 0014 014a 01 # Scroll left



    # readData("0000 0000 0000 0000 0000 0000")
    #
    # sendCommand("0303 0014 0147 00")



    # cleanup()
