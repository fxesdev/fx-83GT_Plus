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

# Hackstrings

## Hackstring Explanation

(This explanation assumes some familiarity with ROP)

A hackstring is just another word for ROP (Return Oriented Programming) payload which
is entered via basic overflow. Hackstrings consist of three parts

[Pre-ROP Padding] [ROP Chain] [Post-ROP Padding]

The Pre-ROP padding is used to align the ROP chain with the stack so it overwrites the
return address. The Post-ROP Padding is to pad the hackstring to a minimum of 100 bytes.
It needs to be minimum 100 bytes long as that is the size of the input area.

When equals is pressed the data in the input area (8154h - 81B8h) to the cache area
(81B8h - 821Ch) using a copy function that terminates when it hits a NULL byte.
Normally this works just fine as the calculator only allows you to enter 99 bytes with the 100th being a NULL. Basic overflow allows overwriting of this NULL byte and since
the cache area lies after the input area, it will copy the 100 bytes of the input buffer
over and over until it hits the end of memory or a sinkhole (ie always reads NULL).

## Entering Hackstrings

(This is specific to the 83GT Plus due to step 2, which I've only found works there)

1. Enter stat submode zero
	1. Press [Mode] [2] to open the stat menu
	2. Press [AC], then a short time later [On]. This will require a few attempts, so keep trying
	3. You can tell you are in stat submode zero if when you enter [Shift] [1] it
	shows "Type, Data, Sum, Var, Reg, MinMax"
2. Enter mode 68
	1. Enter "183[^2][x hat][=]".
		- [^2] is the button directly above [hyp].
		- [x hat] is entered via [Shift] [1] [5] [4] (Only in stat submode 0)
	2. Press [On] when the calculator freezes
3. Now execute basic overflow
	1. Enter "2^(2[=]"
		- ^( is the button next to [^2]
	2. Enter [Shift] [9] [1] [=], to clear setup
	3. Enter [AC] when prompted
	4. Press [Up] [Right] [Right] [Del] [Left] [Del] [Del] [Right] [Right]. You want to 
	delete the 2s and [^(] leaving an empty box with your cursor inside it.
4. Enter the hackstring
	1. Enter the 52 padding characters
	2. Enter the ROP chain
	3. Enter enough characters to ensure being over the 100 bytes
		- Generally I do this by rapidly clicking one of the buttons for about 5 
		seconds
		- If you enter too many bytes cursor will wrap around to the start as the
		variable storing the index is 8 bits. At this point you have to reset the
		calculator and go back to stage 1 (stat submode 0)
	4. Enter [Right] [Right] [0] [Del] [Del]
		- If you've done everything right, you'll be left with a string over 100
		characters with the ROP chain starting at the 53rd character
	5. Press equals