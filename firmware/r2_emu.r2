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
s 0x93d4
af
s 0x3934
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
afn reset_disp      @ 0x3910
afn set_disp_r0     @ 0x3934
afn delay           @ 0x37b4
afn menu            @ 0x9d08

# Fixup weird analysis
s 0x38d4
afm 0x38ea
s 0x2be2
afm 0x2be4
s diag_mode
afm diag_s7
s 0x31a6
afm 0x3188
s 0x3934
afm 0x3910

# Seek to entry point
s entry