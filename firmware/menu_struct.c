#include <stdint.h>

/*
Struct array starts at 222ah

Used by menu (9d08h)
*/

struct entry {
	uint16_t *text;			/* Pointer to text to display. 4 lines separated by NULL bytes */
	uint8_t   sub_menu;		/* Indexed (MSB bit 0) with button press. If 1 return value, if 0 enter sub menu */
	uint8_t   unk;          /* Indexed (MSB bit 0) with button press. If 1 r0 = 2, if 0 r0 = 3 */
	uint8_t buttons[8];	    /* Return value or sub menu index. If bit 7 == 1 and sub_menu == 0, return value with r0 = 1 */
	uint8_t   menu_up;		/* Index of the menu accessed by pressing up */
	uint8_t   menu_down;    /* Index of the menu accessed by pressing down */
	uint8_t   menu_left;	/* Index of the menu accessed by pressing left */
	uint8_t   menu_exit;	/* Keycode signalling exit menu */
};