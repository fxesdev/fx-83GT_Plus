addresses = []
for x in range(33):
	addresses.append(0x8154 + 100*x)

# Load keys
keys = {}
with open("keys", "r") as ifile:
	lineno = 0
	for line in ifile:
		line = line.replace("\n", "")
		lineno += 1

		if line == "":
			continue

		try:
			value, presses = line.split(" ", 1)
			value = int(value.replace("0x", ""), 16)
		except ValueError:
			print(f"[-] Couldn't parse line {lineno} \"{line}\"")

		keys[value] = presses

#addresses = [x - 0x10e for x in addresses]

for x in addresses:
	lower = x & 0xFF
	upper = x >> 8

	if lower in keys.keys() and upper in keys.keys():
		print(f"{x:04x} {x+0x10e:04x}")