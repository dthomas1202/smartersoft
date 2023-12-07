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

from smartersoft.drivers import control_requests

class SmartFadeControl():
    """
    Control mappings for buttons, faders, settings, etc.
    """
    def __init__(self):
        super().__init__()

    def set_fader(self, faderNum, level):
        """
        Sets the level of the given fader.
        """
        # SSSS 0014 0000 [00-ff] # Fader 1 intensity
        # SSSS 0014 0017 [00-ff] # Fader 24 intensity
        self.send_command(control_requests.ControlInterface(
            command=0x14,
            index=self.faderMappings["faders"][faderNum],
            state=level))

    def set_bump(self, faderNum, state):
        """
        Sets the bump state of the given fader.
        """
        # SSSS 0014 0100 00         # bump 1 off
        # SSSS 0014 0100 [01-ff]    # bump 1 on
        # SSSS 0014 0117 00         # bump 24 off
        # SSSS 0014 0117 [01-ff]    # bump 24 on
        self.send_command(control_requests.ControlInterface(
            command=0x14,
            index=self.faderMappings["bumps"][faderNum],
            state=state))

    def set_button(self, btnName, state):
        """
        Sets a buttons state using the mapped name, likely from controlMappings array.
        """
        # SSSS 0014 BBBB 00         # button released
        # SSSS 0014 BBBB [01-ff]    # button pushed
        self.send_command(control_requests.ControlInterface(
            command=0x14,
            index=self.controlMappings[btnName],
            state=state))

    # Additional variations of set_button
    def press_button(self, btnName):
        self.set_button(btnName, True)
    def release_button(self, btnName):
        self.set_button(btnName, False)
    def click_button(self, btnName):
        self.press_button(btnName)
        self.release_button(btnName)
        
    def find_fader_page(self, faderNum):
        """
        Finds the correct fader page given an absolute fader number.
        Returns an array with the page name and the real fader number for the page.
        """
        # Figure out what fader page the fader is on
        for i, page in enumerate(self.faderPages):
            if faderNum < page[0]:
                break

        # Determine the actual fader number for the page
        return [page[1], faderNum - ([(0,)] + self.faderPages)[i][0]]
