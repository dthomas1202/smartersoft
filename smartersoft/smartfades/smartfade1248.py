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

from .smartfade import SmartFade

class SmartFade1248(SmartFade):
    idProduct = 0x0200
    series = "1248"

    numFaders = 48
    # List of the last fader on each page, mapping to the button name for that page.
    faderPages = [(24, "1-24"), (48, "25-48")]

    numMems = 24
    numMemPages = 12

    ## Mappings for 0x14 commands.
    # SSSS 0014 XXXX YY
    faderMappings = {
        "faders": tuple(range(0x0000, 0x0017 + 1)),
        "bumps":  tuple(range(0x0100, 0x0117 + 1)),
        "master_fader":     0x0030, "bump_fader":    0x0031,
        "crossfader_a":     0x0032, "crossfader_b":  0x0033
    }
    controlMappings = {
        "rate":     0x0130, "play":     0x0131, "pause":    0x0132,
        "solo":     0x0133, "blackout": 0x0134, "preview":  0x0135,
        "1-24":     0x0136, "25-48":    0x0137, "clear":    0x0138,
        "memories": 0x0139, "next":     0x013a, "stack":    0x013b,
        "mode":     0x013c, "undo":     0x013d, "copy":     0x013e,
        "rec_seq":  0x013f, "magic":    0x0140, "rec_mem":  0x0141,
        "edit_mem": 0x0142, "snapshot": 0x0143, "exit":     0x0144,
        "back":     0x0145, "menu":     0x0146, "ind_1":    0x0147,
        "ind_2":    0x0148, "right":    0x0149, "left":     0x014a
    }
