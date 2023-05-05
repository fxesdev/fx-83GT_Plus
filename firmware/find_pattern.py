with open("rom_emu.bin", "rb") as data_file:
	data = data_file.read()

#pattern = ["\00", "\\x", "\\y", "\\y", "\\x", "\x00", "\\z", "\00"]
#pattern = ["\\1", "\\B", "\\E", "\\2", "\\3", "\\4", "\\E", "\00", "\\5", "\\B", "\\E"]
#pattern = ["\\1", "\\2", "\\^", "\\3", "\\4", "\\5", "\\6", "\xe1", "\\n", "\\8", "\\n", "\\9", "\\^"]
#pattern = ["\xce", "\xf8", "\x5e", "\xfe", "\\1", "\\2", "\xf4", "\xe1", "\\n", "\xf8", "\\n", "\xf4", "\\x5e", "\\4", "\\5", "\xf8"]

def test_pattern(pattern, test):
	state = {}
	test = list(test)

	for p in pattern:
		if p == "\\?": pass
		elif p.startswith("\\"):
			if p in state:
				if test[0] != state[p]:
					return False
			else:
				state[p] = test[0]
		else:
			if test[0] != ord(p):
				return False
		
		test.pop(0)

		if len(state) != len(set(state.values())): return False

	return True

for x in range(4):
	pattern = ["\x03", "\x00"] + ["\\??"] * x + ["\x00", "\x01"]
	# Run pattern as sliding window through file
	addr = 0
	while len(data) >= len(pattern):
		if test_pattern(pattern, data[:len(pattern)]):
			print(f"Found: {addr:04x}")
		addr += 1
		data = data[1:]