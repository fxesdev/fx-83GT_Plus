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
	length = data[0x12F2 + idx] & 0xF

	# Get bytes
	symbols[idx] = base64.b64encode(data[addr:addr+length]).decode()

with open("symbols.json", "w") as data_file:
	json.dump(symbols, data_file)