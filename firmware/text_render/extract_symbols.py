import struct
import json
import base64

with open("../rom_emu.bin", "rb") as data_file:
	data = data_file.read()

symbols = {}
for idx in range(0x100):
	# Get the address of the symbols
	addr = 0x10F2 + 2*idx
	addr = struct.unpack("<H", data[addr:addr+2])[0]

	# Get the length
	flags = data[0x12F2 + idx] >> 4
	length = data[0x12F2 + idx] & 0xF
	
	if flags != 0xF:
		addr += flags

	chars = data[addr:addr+length]

	if flags == 0xF:
		chars += b"\x28"

	# Get bytes
	symbols[idx] = base64.b64encode(chars).decode()

with open("symbols.json", "w") as data_file:
	json.dump(symbols, data_file)