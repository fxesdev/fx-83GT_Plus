import struct

with open("rom_emu.bin", "rb") as data_file:
	data = data_file.read()

addr = 0x19be2

while True:
	src_addr = struct.unpack("<H", data[addr:addr+2])[0]
	addr += 2

	if src_addr == 0xFFFF: break

	dst_addr, length, src_seg, dst_seg = struct.unpack("<HHBB", data[addr:addr+6])
	addr += 6

	if src_addr & 1 == 1 or dst_addr & 1 == 1:
		print(f"Copy {length:04x}h bytes from {src_addr:04x}h to {dst_addr:04x}h")
	else:
		print(f"Copy {length:04x}h bytes from {src_seg}:{src_addr:04x}h to {dst_seg}:{dst_addr:04x}h")