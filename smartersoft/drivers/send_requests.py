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

from .base import BaseStructure

class SendRequest(BaseStructure):
    """
    Initial 12 byte request.
        
    command:
        Either 0, 1, 2
        0: Status check?
        1: Send command
        2: Detailed status check?
        
    pktSize:
        Size of the following packet, or zero if there is none.
        Little-endian value.
    """
    _fields_ = [
       
        ('command', 'B'),
        ('_', 'B', 0),
        ('pktSize', '<H'),
        ('__', 'Q', 0)
    ]

class SendHeader(BaseStructure):
    """
    Base class for sending data with sequence numbers.
    
    seaNum:
        Sequence number for the packet, should be incremented by 1.
        Little-endian value.
    """
    _fields_ = [
        ('seqNum', '<H', 0)
    ]
