import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

cap = cv2.VideoCapture('video.mov')

if cap.isOpened()== False:
	print("Error opening video file")
	quit()

num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#num_frames = 500

#num_frames = 300
#cap.set(cv2.CAP_PROP_POS_FRAMES, 1500)

# Get frame deltas
deltas = []
_, lframe = cap.read()  
for x in range(num_frames - 1):
	if x % 250 == 0:
		print(f"[*] Calculating delta {x:05d}/{num_frames:05d}")

	# Get the next frame
	ret, frame = cap.read()

	if ret == False:
		print("[-] Error reading frame!")
		quit()

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
pthresh = 2.7
peaks = [x for x in peaks if filtered[x] >= pthresh]

# Merge close peaks
dist = 3
peaks_merged = []

i = 1
p0 = peaks[0]
while i < len(peaks):
	p1 = peaks[i]
	i += 1

	if np.abs(p1 - p0) <= dist:
		new = round((p1 + p0) / 2)
		peaks_merged.append(new)
		p0 = peaks[0]
		i += 1
	else:
		peaks_merged.append(p0)
		p0 = p1

# Append the final point
peaks_merged.append(p0)

# Take midpoints between peaks
midpoints = []
for p0, p1 in zip(peaks_merged[:-1], peaks_merged[1:]):
	midpoints.append(int((p0 + p1) / 2))

print(f"[*] Peak detection done")
print(f"[*] Saving frames ...")

# Save frames at the midpoints
for idx, p in zip(range(len(midpoints)), midpoints):
	cap.set(cv2.CAP_PROP_POS_FRAMES, p)

	if idx % 50 == 0:
		print(f"[*] Saving frame {idx:05d}/{len(midpoints):05d}")

	# Get the frame
	ret, frame = cap.read()

	if ret == False:
		print(f"[-] Error reading frame!")
		quit()
	
	cv2.imwrite(f"frames/{idx}.png", frame)

# Generate signal for graphing
peaks_signal = np.zeros(len(filtered))
for p in peaks:
	peaks_signal[p] = 5

peaks_merged_signal = np.zeros(len(filtered))
for p in peaks_merged:
	peaks_merged_signal[p] = 5

midpoints_signal = np.zeros(len(filtered))
for p in midpoints:
	midpoints_signal[p] = 5

#plt.plot(deltas)
plt.plot(filtered)
plt.plot(mvals)
plt.plot(peaks_signal)
plt.plot(peaks_merged_signal)
plt.plot(midpoints_signal)

plt.savefig('timing_recovery.png')

plt.show()

cap.release()

# Closes all the frames
cv2.destroyAllWindows()