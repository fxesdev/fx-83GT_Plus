import struct

with open("rom_emu.bin", "rb") as data_file:
	data = data_file.read()

def get_string(addr):
	text = b""
	line = 0
	while line < 4:
		if data[addr] == 0:
			text += b"\n"
			line += 1
		else:
			text += bytes([data[addr]])
		
		addr += 1
	
	return text[:-1]

base = 0x222a

def get_entry(idx):
	addr = base + (idx << 4)
	entry = struct.unpack("<HBBBBBBBBBBBBBB", data[addr:addr+16])

	return entry

def traverse_entries(idx):
	entry = get_entry(idx)

	addr = entry[0]
	text = get_string(addr).decode(errors='backslashreplace')
	print(f"[{idx:03d}] {text}")

	mask = entry[1]

	for x in range(0, 8):
		# Sub-menu or text
		if mask >> (7 - x) & 1 == 0:
			traverse_entries(entry[3 + x])
	
	# Next menu
	if entry[12] != 0x00:
		traverse_entries(entry[12])

traverse_entries(0x18)

"""
for idx in range(30):
	entry = get_entry(idx)

	if entry[14] == 0xE6:
		continue

	addr = entry[0]
	text = get_string(addr).decode(errors='backslashreplace')
	print(f"[{idx:03d}] {text}")

	print(entry)
"""