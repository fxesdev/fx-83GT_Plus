import cv2
import numpy as np
import json

img = cv2.imread("overlay.png")

rows, cols, _ = img.shape

print(f"[*] Overlay is {rows}x{cols}")

x = y = 0

pixels = []

while True:
	ix = x
	iy = y

	# Get bounds
	while x < cols and np.array_equal(img[y, x], [0, 0, 255]) == False:
		x += 1
	x -= 1

	while y < rows and np.array_equal(img[y, x], [0, 0, 255]) == False:
		y += 1
	y -= 1

	# Add to array
	pixels.append((ix, iy, x, y))

	# Get next starting pos
	x += 2
	
	if x >= cols:
		x = 0
		y += 2
	else:
		y = iy
	
	if y >= rows:
		break

if len(pixels) != 31 * 96:
	print(f"[-] Incorrect number of pixels!")

# Write to file
with open("overlay.json", "w") as f:
	json.dump(pixels, f)