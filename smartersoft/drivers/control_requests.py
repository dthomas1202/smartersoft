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
from .send_requests import SendHeader

class ControlInterface(BaseStructure):
    """
    7 byte request for any controls, button, faders, etc.
    
    command:
        0x14: Controls physical buttons and faders.
        0x27: Used for info and erase
    
    index:
        Index of the fader, button or command.
    
    state: Level of the fader, or button pushed state.
    """
    _fields_ = [
        ('SendHeader', SendHeader()),
        ('_', 'B', 0),
        ('command', 'B'),
        ('index', 'H'),
        ('state', 'B')
    ]
