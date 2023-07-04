import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

cap = cv2.VideoCapture('video.mov')

if cap.isOpened()== False:
	print("Error opening video file")

#num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

num_frames = 5000

#num_frames = 300
#cap.set(cv2.CAP_PROP_POS_FRAMES, 1500)

# Get frame deltas
deltas = []
_, lframe = cap.read()  
for x in range(num_frames):
	if x % 250 == 0:
		print(f"[*] Calculating delta {x:05d}/{num_frames:05d}")

	# Get the next frame
	ret, frame = cap.read()

	# Calculate the average difference
	diff = cv2.absdiff(lframe, frame)
	deltas.append(np.average(diff))
	
	lframe = frame

# Gaussian filter
size = 6
sigma = 1.75

print(f"[*] Generating gaussian filter kernel")
r = range(-int(size/2),int(size/2)+1)
kernel = [1 / (sigma * np.sqrt(2*np.pi)) * np.exp(-float(x)**2/(2*sigma**2)) for x in r]
kernel /= np.sum(kernel)

print(f"[*] Applying filter kernel")
filtered = np.concatenate(([0] * int(size/2), np.convolve(kernel, deltas, mode='valid'), [0] * int(size/2)))
print(f"[*] Filter kernel applied")

#for x in range(num_frames):
#	print(f"{x} {start_frame+x:03d}->{start_frame+x+1:03d} {deltas[x]:10.7f} {filtered[x]:10.7f} {deltas[x] >= 5}")

print(f"[*] Applying peak detection")
# Peak detection
# Get max value in window around sample
pwidth = 7
off = int(pwidth/2)
mvals = [0] * off
for x in range(off, len(filtered) - off):
	mvals.append(max(filtered[x-off:x+off+1]))

# Find up-down peak matching peak value
peaks = [0]
for x in range(1, len(filtered) - 1):
	if filtered[x - 1] - filtered[x] < 0 and filtered[x] - filtered[x + 1] >= 0 and filtered[x] == mvals[x]:
		peaks.append(x)

peaks.append(0)	# Account for missing point at the end

# Apply a threshold
pthresh = 3
peaks = [x for x in peaks if filtered[x] >= pthresh]

# Generate signal for graphing
peaks_signal = np.zeros(len(filtered))

for p in peaks:
	peaks_signal[p] = 5

# Merge close peaks
dist = 3
peaks_merged = []

p0 = peaks.pop(0)
while len(peaks) > 0:
	p1 = peaks.pop(0)

	if np.abs(p1 - p0) <= dist:
		new = round((p1 + p0) / 2)
		peaks_merged.append(new)
		p0 = peaks.pop(0)
	else:
		peaks_merged.append(p0)
		p0 = p1

# Append the final point
peaks_merged.append(p0)

# Generate signal for graphing
peaks_merged_signal = np.zeros(len(filtered))
for p in peaks_merged:
	peaks_merged_signal[p] = 5

#plt.plot(deltas)
plt.plot(filtered)
plt.plot(mvals)
plt.plot(peaks_signal)
plt.plot(peaks_merged_signal)
plt.show()

cap.release()

# Closes all the frames
cv2.destroyAllWindows()