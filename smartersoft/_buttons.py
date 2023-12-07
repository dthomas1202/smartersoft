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
Any functions that control a physical button.
"""

def set_fader_bump(self, faderNum, state, change_page=False):
    """
    Sets the bump for a given fader.
    If enabled, changes to the right page and sets the fader bump.

    NOTE: Two bumps on different pages can't be active at the same 
    time. In addition, enabling change_page with bumps active will reset
    them, even if there was no change in page.
    """
    if not 0 <= faderNum < self.SmartFade.numFaders:
        raise IndexError("Attempted to access a fader number that does not exist")
    if not 0 <= state <= 255:
        raise ValueError("Attempted to set a fader bump to a value outside its range")

    if change_page:
        faderNum = self.goto_fader_page(faderNum)
    else:
        _, faderNum = self.SmartFade.find_fader_page(faderNum)
        
    self.SmartFade.set_bump(faderNum, state)
    
def set_memory_bump(self, memNum, state, memPage=None, change_page=False):
    """
    Sets the state of a given memory or sequence bump on a memory page.
    If enabled, changes to the right page and sets the bump.

    NOTE: Two bumps on different pages can't be active at the same 
    time. In addition, enabling change_page with bumps active will reset
    them, even if there was no change in page.
    """
    if not 0 <= memNum < self.SmartFade.numMems:
        raise IndexError("Attempted to access a memory bump number that does not exist")
    if not 0 <= state <= 255:
        raise ValueError("Attempted to set a memory bump to a value outside its range")
    if not 0 <= memPage < self.SmartFade.numMemPages and change_page == True:
        raise IndexError("Attempted to access a memory page number that does not exist")

    if change_page:
        self.goto_memory_page(memPage)

    self.SmartFade.set_bump(memNum, state)

def goto_fader_page(self, faderNum):
    """
    Switches to the correct page for the fader.
    Returns the real fader number for the page.
    """
    if not 0 <= faderNum < self.SmartFade.numFaders:
        raise IndexError("Attempted to access a fader number that does not exist")
    
    # Figure out where the fader is
    pageName, relFaderNum = self.SmartFade.find_fader_page(faderNum)
    
    self.SmartFade.click_button(pageName)
    
    return relFaderNum

def goto_memory_page(self, memPage):
    """
    Switches to the given memory page by pressing and holding the
    memories button, then clicking a bump to switch to that page.
    """
    if not 0 <= memPage < self.SmartFade.numMemPages:
        raise IndexError("Attempted to access a memory page number that does not exist")
    
    # Hold the memory button and select the memory page
    self.SmartFade.press_button("memories")
    self.SmartFade.set_bump(memPage, True)
    self.SmartFade.set_bump(memPage, False)
    self.SmartFade.release_button("memories")

