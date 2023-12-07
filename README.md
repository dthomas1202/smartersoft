# SmarterSoft

> Is your venue or school rocking gear so 'vintage' it makes you wonder if dinosaurs used DMX512?
>
> Do you find yourself trapped using a software time machine that seems to believe Windows XP was the pinnacle of UI design?
>
> Is your director breathing down your neck, demanding ambitious lighting effects that would make a modern console shiver?
>
> Well hold my spotlight, because SmarterSoft is here to make your creating your lighting control dreams... marginally less terrible!
>
> Ever wanted scripted control over your SmartFades outputs?
> SmarterSoft's got your back... well, most of the time... because who doesn't love a little unpredictability in their lighting performance?

SmarterSoft is a Python library for interfacing with ETC SmartFade consoles via USB.
SmarterSoft uses the same protocol that ETC's SmartSoft control software uses, although reverse engineered from packet captures.

Reverse engineering efforts were based off of the SmartFade 1248 and packet captures between SmartSoft v3.0.2, and as such this is the only console that is currently supported.
In theory, based on the what can be understood about the protocol, it should be possible to make some assumptions about the control scheme of other SmartFades.

# Features and Usage
This library is nowhere near complete, and most functions have had very little testing, although everything should more or less work.
As of writing, I no longer have access to a console for development, so this library is presented as is for the forseeable future.

**USE AT YOUR OWN RISK**

Currently supported functions include:

- set_fader(faderNum, level, change_page=False)
- set_memory(memNum, level, memPage=None, change_page=False)
- set_fader_bump(faderNum, state, change_page=False)
- set_memory_bump(memNum, state, memPage=None, change_page=False)
- goto_fader_page(faderNum)
- goto_memory_page(memPage)

Check docstrings for more information.

See [example.py](example.py) for a short demonstration.

# Unimplemented Protocol
If you just love deciphering other peoples garbage, check out [test.py](test.py).
This contains the basic functions that were used to reverse engineer the protocol.
In addition, there are also descriptions of the protocol as well as unimplemented parts of it.

*Have fun*

# License
GNU General Public License v3.0 (GNU GPLv3)
