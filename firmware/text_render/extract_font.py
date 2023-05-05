import numpy as np
from PIL import Image

with open("../rom_emu.bin", "rb") as data_file:
	data = data_file.read()

fonts = {
	7: (0x400, 0x746, 6, 0x1f, 1),
	5: (0x22, 0x707, 9, 0x1f, 0)
}

font = fonts[5]

characters = []
for r0 in range(0x100):
	output = []

	# Lookup table
	addr = font[0]
	r8 = font[2]

	if r0 < 0x20:
		# Different lookup table?
		addr = font[1]
		r0 += font[3]
		r0 &= 0xFF
		r8 += font[4]
	
	# This is hardcoded for some reason
	if r0 == 0x7C:
		output = [0xC0] * r8
	else:
		# Convert from character code to lookup in table
		r0 += 0xE0
		r0 &= 0xFF
		r0 *= 5
		r4 = r0 & 0b111
		r0 >>= 3
		r0 *= r8

		addr += r0

		# Read all of the rows
		for _ in range(r8):
			# Read character map
			r0 = data[addr]
			addr += 1

			r0 = (r0 << r4) & 0xFF
			r0 >>= 1

			r1 = 8 - r4
			
			# Not really sure what this does
			if r1 < 5:
				er6 = addr
				er6 += r8
				er6 -= 1
				r1 = data[er6]
				r6 = 9 - r4
				r1 >>= (r6 & 0b111)

				r0 |= r1
			
			r0 &= 0x7c # 0b1111100
			output.append(r0)

			# There's an inc here which makes no sense
			# as the address is located in rom???
	
	# Convert into a numpy array
	output = np.array([[(row >> (7-p) & 1) ^ 1 for p in range(8)] for row in output])
	characters.append(output)

# Stitch together into one big array
rows = []
for x in range(16):
	row = np.hstack(list(characters[16*x + i] for i in range(16)))
	rows.append(row)
image = np.vstack(rows) * 255

img = Image.fromarray(image.astype("uint8"), mode="L").convert("1")
img.save("font.png")