import json
from PIL import Image
import base64
import os

sizeX = 8
sizeY = 9

# Create folder for the symbols
if not os.path.isdir("symbols"):
	os.mkdir("symbols/")

# Load symbol-character mapping
symbols = {}
with open("symbols.json", "r") as data_file:
	data = json.load(data_file)

	for k, v in data.items():
		symbols[int(k)] = list(base64.b64decode(v))

# Load the font and extract the individual images
chars = []
with Image.open("font.png") as font:
	for y in range(16):
		for x in range(16):
			chars.append(font.crop((sizeX*x, sizeY*y, sizeX*(x+1), sizeY*(y+1))))

# Loop over all symbols
for k, v in symbols.items():
	# Create an image to hold the symbol
	sym_im = Image.new("1", (sizeX * len(v), sizeY))

	# Concatenate all the individual symbols
	for c,i in zip(v, range(len(v))):
		sym_im.paste(chars[c], (sizeX * i, 0))

	sym_im.save(f"symbols/{k:02X}.png")