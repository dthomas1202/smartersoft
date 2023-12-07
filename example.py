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

import smartersoft
import time

sf = smartersoft.SmarterSoft()
state = True

# Set every other fader to 100% on the first page
# and swap them every second.
while True:
    for i in range(0, 23, 2):
        sf.set_fader(i, state * 255)
        sf.set_fader(i + 1, (not state) * 255)

    state = not state
    time.sleep(1)
