import struct

with open("rom_emu.bin", "rb") as data_file:
	data = data_file.read()

interrupts = [
	(0x0008, "WDTINT"),
	(0x000a, "XI0INT"),
 	(0x000c, "XI1INT"),
	(0x000e, "XI2INT"),
	(0x0010, "XI3INT"),
	(0x0012, "TM0INT"),
	(0x0014, "L256SINT"),
	(0x0016, "L1024SINT"),
	(0x0018, "L4096SINT"),
	(0x001a, "L16384SINT"),
	(0x001c, "SIO0INT"),
	(0x001e, "I2C0INT"),
	(0x0020, "I2C1INT"),
	(0x0022, "BENDINT"),
	(0x0024, "BLOWINT"),
	(0x0026, "RTCINT"),
	(0x0028, "AL0INT"),
	(0x002a, "AL1INT")
]

for i,n in interrupts:
	addr = struct.unpack("<H", data[i:i+2])[0]
	print(f"{addr:04x} {n}")