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

from smartersoft.drivers import send_requests
import usb.core
import usb.util
import os

class SmartFadeUSB():
    """
    Raw USB interfacing with the SmartFade.
    """
    maxSeqNum = 65535
    
    def __init__(self):
        super().__init__()
        self.usbDev = None

        # In/Out relative to host
        self.usbDataIn = None
        self.usbDataOut = None

        self._usbSeqNum = 0
        
    @property
    def usbSeqNum(self):
        """
        USB sequence number for packets that use it.
        """
        return self._usbSeqNum
    
    @usbSeqNum.setter
    def usbSeqNum(self, value):
        self._usbSeqNum = value % (self.maxSeqNum + 1)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    # Attempts to find the usb device, and claims the useful
    # interfaces if found.
    # Returns True if found, otherwise False
    def find_dev(self, index=0):
        print(f"Looking for SmartFade {self.series} #{index} ({hex(self.idVendor)}:{hex(self.idProduct)})")

        # Find all matching usb devices
        devs = list(usb.core.find(find_all=True, idVendor=self.idVendor, idProduct=self.idProduct))

        # Was any found?
        if len(devs) <= index:
            print(f"SmartFade {self.series} #{index} ({hex(self.idVendor)}:{hex(self.idProduct)}) Not Found")
            return False

        self.usbDev = devs[index]
        return True

    # Claim useful interfaces from the kernel
    # Returns True on success, False on failure or if os is Windows
    def claim_dev(self):
        # Return early if running on Windows
        if os.name == 'nt':
            return False

        for cfg in self.usbDev:
            for intf in cfg:
                if self.usbDev.is_kernel_driver_active(intf.bInterfaceNumber):
                    try:
                        print(f"Detatching kernel driver from interface {intf.bInterfaceNumber}")
                        self.usbDev.detach_kernel_driver(intf.bInterfaceNumber)
                    except usb.core.USBError as e:
                        print(f"Could not detatch kernel driver from interface {intf.bInterfaceNumber}: {str(e)}")

                print(f"Claiming interface {intf.bInterfaceNumber}")
                usb.util.claim_interface(self.usbDev, intf.bInterfaceNumber)

    # Relase useful interfaces back to the kernel
    # Returns True on success, False on failure or if os is Windows
    def release_dev(self):
        # Return early if running on Windows
        if os.name == 'nt':
            return False

        for cfg in self.usbDev:
            for intf in cfg:
                print(f"Releasing interface {intf.bInterfaceNumber}")
                usb.util.release_interface(self.usbDev, intf.bInterfaceNumber)

    # Sets up our usb endpoints
    def find_endpoints(self):
        intf = self.get_data_interface(self.get_dev_cfg(self.usbDev))

        self.usbDataIn = self.get_data_in_endpoint(intf)
        self.usbDataOut = self.get_data_out_endpoint(intf)

    # Returns the currently set configuration.
    # If no configuration is set the first one is selected with no arguments,
    # otherwise the configuration parameter is the bConfigurationValue field of the
    # configuration you want to set as active.
    def get_dev_cfg(self, dev, configuration=None):
        cfg = dev.get_active_configuration() # Get active configuration
        if cfg is None or configuration is not None:
            # Reset the device into a known state
            dev.reset()
            # Set the active configuration. With no arguments, the first
            # configuration will be the active one
            dev.set_configuration(configuration)
            cfg = dev.get_active_configuration() # Get new active configuration
        return cfg

    # Returns the interface used for data transactions
    def get_data_interface(self, cfg):
        return usb.util.find_descriptor(cfg, bInterfaceClass=255)

    # Returns the endpoint for device to host communication (Endpoint 3)
    def get_data_in_endpoint(self, dataIntf):
        return usb.util.find_descriptor(dataIntf, bEndpointAddress=0x83)

    # Returns the endpoint for host to device communication (Endpoint 4)
    def get_data_out_endpoint(self, dataIntf):
        return usb.util.find_descriptor(dataIntf, bEndpointAddress=0x04)

    def send_command(self, data):
        self.usbDataOut.write(send_requests.SendRequest(command=0x01, pktSize=data.calc_size()).pack())

        data.SendHeader.seqNum = self.usbSeqNum
        self.usbDataOut.write(data.pack())

        self.usbSeqNum += 1

    def _empty_buffer(self):
        while True:
            cmd = send_requests.SendRequest(command=0x00, pktSize=0)
            self.usbDataOut.write(cmd.pack())

            data = self.usbDataIn.read(cmd.calc_size())
            print(data)
            cmd.unpack(data)

            if cmd.pktSize == 0:
                break

            print(self.usbDataIn.read(cmd.pktSize)) 
