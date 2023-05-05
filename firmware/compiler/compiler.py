import argparse
import re

parser = argparse.ArgumentParser(
	prog = 'Hackstring Compiler'
)

parser.add_argument(
	'-g', '--gadgets',
	default = 'gadgets'
)
parser.add_argument(
	'-k', '--keys',
	default = 'keys'
)
parser.add_argument(
	'-u', '--unstable',
	action = 'store_true'
)
parser.add_argument(
	'input file'
)

args = parser.parse_args()

# Load keys
keys = {}
try:
	with open(args.keys, "r") as ifile:
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
except FileNotFoundError:
	print(f"[-] Couldn't find keys file \"{args.keys}\"")
	exit()

print(f"[+] Loaded {len(keys.keys())} keys from file \"{args.keys}\"")

# Load gadgets
# TODO: Implement gadgets

# Utility function for getting value matching bit pattern
def key_mask(string):
	# Check which bits matter
	mask = re.sub("[^x]", "f", string)
	mask = mask.replace("x", "0")
	mask = int(mask, 16)

	value = int(string.replace("x", "0"), 16)

	for x in keys.keys():
		if value == x & mask:
			return x
	
	print(f"[-] No key with value 0x{value:02x}")
	return None

def compile(hackstring):
	# Replace padding and don't matter bits
	hackstring = hackstring.replace("xx", "2e")
	hackstring = hackstring.split(" ")

	length = len(hackstring)
	
	# Convert value to keypresses
	hackstring = [key_mask(x) if "x" in "x" else int(x, 16) for x in hackstring]

	if None in hackstring:
		return (0, None)
	
	return (length, " ".join([keys[x] for x in hackstring]))

# Compile hackstring
#hackstring = "xx xx 60 39 x0 xx 8c 29 x0 xx 39 60 xx xx be 70 x0 xx 57 81 74 34 x0 xx xx xx xx xx 60 39 x0 xx"
#hackstring = "xx xx 60 39 x0 xx 8c 29 x0 xx 60 39 xx xx be 70 x0 xx 57 81 60 39 x0 xx"
#hackstring = "xx xx 60 39 x0 xx 8c 29 x0 xx 60 39 xx xx 60 39 x0 xx"
#hackstring = "xx xx 60 39 x0 xx 58 39 x0 xx 57 81 xx xx xx xx xx xx 60 39 x0 xx"
#hackstring = "xx xx 60 39 x0 xx 74 34 x0 xx xx xx xx xx 60 39 x0 xx"

"""
#          Pad   Diag Mode   pop er14          sp = er14
payload = "xx xx 60 39 x0 xx 74 74 x0 xx 54 81 72 74 x0 xx"

#         Pop qr0     er0   er2   er4   er6   pop er14          sp = er14
loader = "58 39 x0 xx xx xx xx xx 60 39 x0 xx 74 74 x0 xx 54 81 72 74 x0 xx"
"""

"""
#          Pad
payload = "xx xx 60 39 x0 xx"

#         Pop qr0     er0   er2   er4   er6   pop er14          sp = er14     diag_mode   pop er14          sp = er14
loader = "58 39 x0 xx xx xx xx xx 60 39 x0 xx 74 74 x0 xx 54 81 72 74 x0 xx" #60 39 x0 xx 74 74 x0 xx b0 86 72 74 x0 xx"
"""

"""
payload = "xx xx 60 39 x0 xx" #74 74 x0 xx a0 85 72 74 x0 xx"

#         Pop qr0     er0   er2   er4   er6   diag_mode   pop er14          sp = er14
loader = "58 39 x0 xx xx xx xx xx 60 39 x0 xx 60 39 x0 xx 74 74 x0 xx 54 8b 72 74 x0 xx"
"""

payload = ""

#         Pop er0                 Delay       set lr      screen_update + 0xa                 er14              diag_mode   sp = er14
#loader = "8c 29 x0 xx 30 30 xx xx a9 36 x0 xx 8b 33 x1 xx 92 2d x0 xx 30 30 xx xx xx xx xx xx 86 81 xx xx xx xx 60 39 x0 xx 72 74 x0 xx"

#         Pop er0                 Delay       set lr      pop er14    er14  diag_mode   sp = er14
loader = "8c 29 x0 xx 30 30 xx xx a9 36 x0 xx 8b 33 x1 xx 3a 42 x0 xx xx xx 60 39 x0 xx 72 74 x0 xx"

if payload == "":
	p_len = 0
else:
	p_len, payload = compile(payload)

if payload == None:
	print("[+] Error in payload")
	exit()

if p_len > 52:
	print("[-] Payload too big")
	exit()

l_len, loader = compile(loader)

if payload == None:
	print("[-] Error in loader")
	exit()

if l_len > (100 - 52):
	print("[-] Loader too big")
	exit()

hackstring = payload							# Payload
hackstring += f" {(52 - p_len)}^[.] "			# Pad to entry (ie 52 bytes)
hackstring += loader							# Loader
hackstring += f" {(100 - 52 - l_len)}^[.]"		# Pad to 100 bytes

print(hackstring)