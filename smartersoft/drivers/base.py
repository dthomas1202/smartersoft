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

class BaseStructure():
    """
    Base class for raw urb usb requests. Create child classes
    with a _fields_ attribute containing a list of tuples. Each tuple contains either up-to 3
    values, the first is the name of the created attribute. The second is the
    struct format code, and the optional third is the default
    value. Or 2 values, the first is still the name, the second is an instance of another child class to inherit from.
    Note that two names cannot be the same.
    """
    
    byteOrderCodes = "@=<>!"
    defaultByteOrder = ">" # Big-endian (MSB first)

    def __init__(self, **kwargs):
        """
        Takes any named arguments passed to __init__, and
        parameters with default values from the child classes
        _fields_ and adds them as attributes to the class.
        """
        for field in self._fields_:
            if isinstance(field[1], (BaseStructure)):
                setattr(self, field[0], field[1])
            elif len(field) > 2:
                setattr(self, field[0], field[2])

        self.add_attrs(**kwargs)
    
    def add_attrs(self, **kwargs):
        """
        Takes given named arguments and adds them as attributes to the class.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def calc_format(self):
        """
        Combine this and all child format codes into a single string.
        Uses the value of defaultByteOrder if no byte order is given.
        If the format code is an instance we can call this function
        on it, and append the results to the string.
        """
        format_codes = ""
        for field in self._fields_:
            if isinstance(field[1], (BaseStructure)):
                format_codes += field[1].calc_format()
            else:
                format_codes += self.add_missing_boc(field[1])
        return format_codes

    def calc_size(self):
        """
        Calculate the total size of this and all child structures.
        """
        size = 0
        for field in self._fields_:
            if isinstance(field[1], (BaseStructure)):
                size += field[1].calc_size()
            else:
                size += struct.calcsize(self.add_missing_boc(field[1]))
        return size
    
    def has_boc(self, formatString):
        """
        Checks if the given formatString has any chars from byteOrderCodes.
        """
        return any(i in formatString for i in self.byteOrderCodes)

    def add_missing_boc(self, formatString):
        """
        Adds the defaultByteOrder code if one is missing to start of the formatString.
        """
        if self.has_boc(formatString):
            return formatString
        else:
            return self.defaultByteOrder + formatString


    def pack(self):
        """
        
        """
        buf = b""
        for field in self._fields_:
            if isinstance(field[1], (BaseStructure)):
                buf += getattr(self, field[0]).pack()
            else:
                buf += struct.pack(self.add_missing_boc(field[1]), getattr(self, field[0]))

        return buf

    def unpack(self, buf):
        """
        
        """
        if self.calc_size() != len(buf):
            raise ValueError(f"Unpack requires a buffer length of {self.calc_size()} byte(s)")

        for field in self._fields_:
            if isinstance(field[1], (BaseStructure)):
                size = field[1].calc_size()
                field[1].unpack(buf[:size])
            else:
                size = struct.calcsize(field[1])
                setattr(self, field[0], struct.unpack(self.add_missing_boc(field[1]), buf[:size])[0])

            buf = buf[size:] 
