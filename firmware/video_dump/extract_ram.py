import cv2
import numpy as np
import statistics as stats
import json

## Load the frames
#cap = cv2.VideoCapture("frames_post/%04d.png", cv2.CAP_IMAGES)
#
#if cap.isOpened()== False:
#	print("Error opening image sequence")
#	quit()
#
#num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#
## Load the overlay
#with open("overlay/overlay.json", "r") as fp:
#	overlay = json.load(fp)
#
## Loop over all the frames and extract the bits
#frames = []
#for x in range(num_frames):
#	if x % 50 == 0:
#		print(f"[*] Extracting bits {x:05d}/{num_frames:05d}")
#
#	# Get the frame
#	ret, img = cap.read()
#
#	if ret == False:
#		print("[-] Error reading frame!")
#		quit()
#
#	# Apply the overlay
#	bits = []
#	for x0, y0, x1, y1 in overlay:
#		val = np.average(img[y0:y1, x0:x1])
#
#		bits.append(val)
#
#	# Threshold the bits
#	bits = [1 if x < 120 else 0 for x in bits]
#
#	# Convert bits to bytes
#	frame = []
#	for i in range(31 * 12):
#		byte = sum([x << idx for x,idx in zip(bits[8*i:8*(i+1)][::-1], range(8))])
#		frame.append(byte)
#
#	frames.append(frame)

with open("data.json", "r") as f:
	frames = json.load(f)

# Find "EC 8D" which only appears at the start of the ROM
start_offsets = []
for i in range(len(frames)):
	for x in range(371):		# (31 * 96)/2 - 1
		if frames[i][x:x+2] == [0xEC, 0x8D]:
			start_offsets.append((i, x))
			print(f"[*] Found ROM start @ frame {i:03d}+{x:02x}")

# Get data memory with holes
data_mem = [[] for x in range(0x10000)]

for start, end in zip(start_offsets[:-1], start_offsets[1:]):
	if end[0] - start[0] < 170:
		print(f"[*] Found region {start} - {end}")

		# Get the frames
		data = []
		for i in range(end[0] - start[0]):
			f = frames.pop(start[0])
			data += f
			data += [None] * 12

		# Remove offset
		data = data[start[1]:]

		for i in range(len(data)):
			if data[i] != None:
				data_mem[i].append(data[i])

		break

# Run the other frames over the data in a sliding window
# and perform correlation, ignoring empty addresses
idx = 0
frame = frames.pop(0)
while len(frames) > 0:
	idx += 1
	print(f"[*] Correlating frame {idx}")

	# Correlate the frame
	corr_addrs = []
	for addr in range(0x8E00):
		matching = 0
		for x in range(372):
			offset = addr + x - 371

			# If there is data there already, does it match?
			if frame[x] in data_mem[offset]:
				matching += 1
		
		corr_addrs.append((matching, addr))
	
	# Filter the correlations
	corr_addrs = sorted(corr_addrs, key=lambda x:x[0], reverse=True)
	matching, addr = corr_addrs[0]

	if matching < 250:
		#for x in range(372):
		#	offset = addr + x - 371
		#	
		#	print(f"{frame[x]} {data_mem[offset]}")

		for x in frame:
			print(f"{x:02x} ", end = "")
		print("")

		print(corr_addrs[:10])

		print(f"[-] No remotely good correlation???")
		quit()

	# Add the data to memory
	for x in range(372):
		offset = addr + x - 371

		data_mem[offset].append(frame[x])
	
	addr += 13

	# Try the next frames
	while len(frames) > 0:
		frame = frames.pop(0)

		idx += 1
		print(f"[*] Correlating frame {idx}")

		# Correlate the frame
		matching = 0
		for x in range(372):
			if frame[x] in data_mem[addr + x]: matching += 1

		# Are we still matching well?
		if matching <= 340:

			print("[*] Correlation lost")
			break

		# Add the data to memory
		for x in range(372):
			data_mem[addr + x].append(frame[x])
		
		addr += 372 + 12

# Get the "certainty" for each address
certainty = [len(set(x))/len(x) if x != [] else -1 for x in data_mem]

print(certainty)
print(max(certainty))

# Take the mode for each address
data_mem = [stats.mode(x) if x != [] else 0 for x in data_mem]

with open("data.bin", "wb") as f:
	f.write(bytes(data_mem))