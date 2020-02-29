from cffi import FFI
ffibuilder = FFI()

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("""
    void roll_out(uint8_t *game_board, int seed);
    uint8_t *move_up(uint8_t *game_board);
    uint8_t *move_down(uint8_t *game_board);
    uint8_t *move_left(uint8_t *game_board);
    uint8_t *move_right(uint8_t *game_board);
    uint32_t get_time(void);
""")

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
ffibuilder.set_source("_lib2048",
	"""
	#include "lib2048.h"
	""",
	sources=['lib2048.c'],
    libraries=['m'])   # library name, for the linker

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)