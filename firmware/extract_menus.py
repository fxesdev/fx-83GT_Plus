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

for idx in range(30):
	addr = base + (idx << 4)
	entry = struct.unpack("<HBBBBBBBBBBBBBB", data[addr:addr+16])

	addr = entry[0]

	if addr == 0:
		print(f"[{idx:03d}] NULL")
	else:
		text = get_string(addr).decode(errors='backslashreplace')
		print(f"[{idx:03d}] {text}")