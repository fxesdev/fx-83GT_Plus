# fx-83GT Plus Firmware

This folder contains analysis of the firmware. Currently we only have ROM dumps from the emulator,
which has some differences from the actual hardware

Most of this is just going to be my ideas, not necessarily presented
in a pretty way

radare2 is being used along with a [plugin](https://github.com/fraserbc/u8_r2_plugin) that adds
support for the nX-U8 architecture

r2_emulator.r2 is a script that will set function names. It is use like this

`r2 -i r2_emu.r2 -a u8 rom_emu.bin`

Ideally we would use projects but as they are broken currently,
this is a good workaround