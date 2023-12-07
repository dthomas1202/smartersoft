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

from .smartfades import SmartFade

class SmarterSoft():
    """
    High level user class for interacting with a SmartFade.
    """
    from ._buttons import set_fader_bump, set_memory_bump, goto_fader_page, goto_memory_page
    from ._faders import set_fader, set_memory

    def __init__(self, series=None, index=0):
        """
        Finds a connected SmartFade.
        Optionally specify the series name to only select certain SmartFades.
        Or optionally the index to connect to the n'th of the same series.
        """
        self.SmartFade = None

        for smartfade in SmartFade().smartfades:
            if smartfade.series != series and series != None:
                continue

            sf = smartfade()

            if sf.find_dev(index):
                self.SmartFade = sf
                self.SmartFade.claim_dev()
                self.SmartFade.find_endpoints()
                self.SmartFade.on_connect()

                print(f"Found a SmartFade {self.SmartFade.series}")
                return

        print("Did not find a SmartFade")
        
    def __enter__(self):
        """
    
        """
        return self

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        """
    
        """
        self.close()

    def close(self):
        """
        
        """
        self.SmartFade.on_disconnect()
        self.SmartFade.release_dev()
