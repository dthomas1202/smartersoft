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

from .usb import SmartFadeUSB
from .controls import SmartFadeControl

class SmartFade(SmartFadeUSB, SmartFadeControl):
    """
    Base class for all SmartFades control properties.
    """
    idVendor = 0x14d5

    @property
    def smartfades(self):
        """
        Can be used to find all SmartFade series automatically.
        Returns a list of Smartfade series classes.
        """
        return self.__class__.__subclasses__()
