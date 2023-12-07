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

"""
Contains anything that is used to control faders,
crossfaders, master, bump, etc.
"""

def set_fader(self, faderNum, level, change_page=False):
    """
    Sets a given fader to a level between 0-255.
    If enabled, changes to the right page and sets the fader.
    """
    if not 0 <= faderNum < self.SmartFade.numFaders:
        raise IndexError("Attempted to access a fader number that does not exist")
    if not 0 <= level <= 255:
        raise ValueError("Attempted to set a fader to a value outside its range")

    if change_page:
        faderNum = self.goto_fader_page(faderNum)
    else:
        _, faderNum = self.SmartFade.find_fader_page(faderNum)
        
    self.SmartFade.set_fader(faderNum, level)

def set_memory(self, memNum, level, memPage=None, change_page=False):
    """
    Sets a given memory or sequence on a memory page to a level between 0-255.
    If enabled, changes to the right page and sets the memory.
    """
    if not 0 <= memNum < self.SmartFade.numMems:
        raise IndexError("Attempted to access a memory fader number that does not exist")
    if not 0 <= level <= 255:
        raise ValueError("Attempted to set a memory fader to a value outside its range")
    if not 0 <= memPage < self.SmartFade.numMemPages and change_page == True:
        raise IndexError("Attempted to access a memory page number that does not exist")

    if change_page:
        self.goto_memory_page(memPage)

    self.SmartFade.set_fader(memNum, level)
