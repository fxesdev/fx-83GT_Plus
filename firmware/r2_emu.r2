# Recursively analyse at entry point
s 0x39aa
af
afr

# Define functions radare didn't find
s 0x2c24
af
s 0x2d56
af
s 0x2ec2
af
s 0xaee6
af

# Name functions
afn entry           @ 0x39aa
afn ret_0006        @ 0x0006
afn diag_s7         @ 0x3a0e
afn diag_ac         @ 0x3a38
afn diag_mode       @ 0x3a6c
afn screen_update   @ 0x2e96
afn screen_clear    @ 0x2aa2
afn clear_KO        @ 0x395e
afn init_display    @ 0x38d4
afn need_reset      @ 0x371a
afn wake_stop_ki    @ 0x394e
afn memset          @ 0x7e0c
afn zero_mem        @ 0x361c
afn screen_contrast @ 0x38ea
afn read_pd         @ 0x31f0
afn zero_input      @ 0xaeda
afn zero_cache      @ 0xaee6

# Fixup weird analysis
s 0x38d4
afm 0x38ea
s 0x2be2
afm 0x2be4
s diag_mode
afm diag_s7

# Seek to entry point
s entry