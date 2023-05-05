import struct
import string

with open("rom_emu.bin", "rb") as data_file:
	data = data_file.read()

alphabet = set(string.printable + " ") - set(string.whitespace)
alphabet = str(alphabet).encode()
def get_string(addr):
	text = ""
	line = ""
	count = 0
	length = 0
	while count <= 3:
		char = data[addr]
		addr += 1
		length += 1

		if char != 0:
			if char in alphabet:
				char = chr(char)
			else:
				char = f"\\x{char:02x}"
			line += char
		
		if length == 16: addr += 1
		if char == 0 or length == 16:
			text += line + "\n"
			line = ""
			count += 1
			length = 0

	return text

base = 0x222a

def get_entry(entry_addr):
	entry = struct.unpack("<HBBBBBBBBBBBBBB", data[entry_addr:entry_addr+16])

	return entry

def traverse_entries(entry_addr, print_cb = None, path = [], seen = []):
	entry = get_entry(entry_addr)

	seen.append(entry_addr)

	if print_cb != None:
		print_cb(entry_addr, entry, path)
	else:
		addr = entry[0]
		text = get_string(addr)
		print(f"[{entry_addr:04x}] {text}")

	mask = entry[1]

	# Accessible sub menus
	menus = [
		("up", entry[11]),
		("down", entry[12]),
		("left", entry[13])
	]

	for x in range(0, 8):
		# Sub-menu or text
		if mask >> (7 - x) & 1 == 0:
			menus.append((str(x + 1), entry[3 + x]))
	
	menus = [x for x in menus if x[1] & 0x80 == 0]

	# Next menu
	for p, m in menus:
		m = base + (m << 4)
		if m == 0: continue
		if m in seen: continue
		traverse_entries(m, print_cb, path + [p], seen)

def print_cb(entry_addr, entry, path):
	values = []
	for x in range(0, 8):
		if entry[1] >> (7 - x) & 1: values.append((str(x + 1), entry[3 + x]))
	
	for x, n in zip(list(range(0, 3)), ["up", "down", "left"]):
		if entry[11 + x] & 0x80 == 1: values.append((n, entry[11 + x]))

	#if not True in [x in values for x in [0x6E, 0x6F, 0x7E, 0x7F, 0x61, 0x62]]: return

	addr = entry[0]
	text = get_string(addr)
	path = ' '.join(path)
	print(f"[{entry_addr:04x}]")
	print(f"[{path}]")
	print("  ".join([f"{x[0]}: {x[1]:02x}" for x in values]))
	print(text)

#addr = base + (236 << 4)
#addr = 0x23da    BASE-N Shift+3 Menu

# 189^2[x-hat] submode zero
#addr = 0x1ae4
#addr = 0x1af0
#addr = 0x1b04

# 194^2[x-hat] submode zero
#addr = 0x30ea
addr = 0x242a
#addr = 0x243a


"""
0x7e27 text for weird BE....E screen
"""

#traverse_entries(addr, print_cb)
traverse_entries(addr, print_cb)

"""
for idx in range(1024):
	addr = base + (idx << 4)
	entry = get_entry(addr)

	if entry[0] != 0x100: continue
	if entry[11] != 1: continue
	print(f"{addr:04x}")

	#text = get_string(entry[0])
	#print(f"[{addr:04x}] {text}")
	#print(entry)
"""