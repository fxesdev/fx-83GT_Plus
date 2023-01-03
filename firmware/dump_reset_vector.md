# Set ER0 = 0
Emulator: 0:4348
Calc: 0:423a

mov er0, #0h
rt

# Set ER2 = ER0
Emulator: 0:8b54
Calc: 0:8a46

add r4, #ffh
sub r0, r8
subc r1, r9
mov er2, er0
mov r0, r4
mov r1, #0h
pop xr4
rt

# Write to screen
Emulator: 0:3acc
Calc: 0:39be