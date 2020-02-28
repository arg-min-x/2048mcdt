import tools2048
import numpy as np
from cffi import FFI

# game_board = [[2, 16, 2, 0],
#               [4, 32, 2, 0],
#               [8, 128, 64, 0],
#               [16, 512, 0, 0]]
game_board = [[2, 2, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
game_board = np.array(game_board, dtype='uint16')
# game_board = game_board.reshape(16,)

x = 0
seed = 0
for ind in range(100):
      # game_board = [[2, 2, 0, 0],
      #             [0, 0, 0, 0],
      #             [0, 0, 0, 0],
      #             [0, 0, 0, 0]]
      # game_board = np.array(game_board, dtype='uint16')
      # print(game_board)
      tmp = tools2048.roll_out_c(game_board)
      x += tmp
print(x/100)

# x = 0
# game_board = [[2, 2, 0, 0],
#                   [0, 0, 0, 0],
#                   [0, 0, 0, 0],
#                   [0, 0, 0, 0]]
# game_board = np.array(game_board, dtype='uint16')
# for ind in range(100):
# 	x += tools2048.roll_out(game_board)
# print(x/100)

# # Define C data
# ffi = FFI()
# g_board = ffi.new('uint8_t tmp[16]')
# for i in range(16):
#     g_board[i] = game_board[i]

# for i in range(16):
#     print(g_board[i])
# print('')

# # Play out random oves
# tools2048.lib.roll_out(g_board)

# for i in range(16):
#     print(g_board[i])
# print('')
# game_board = [[2, 2, 0, 0],
#                   [0, 0, 0, 0],
#                   [0, 0, 0, 0],
#                   [0, 0, 0, 0]]
# game_board = np.array(game_board, dtype='uint16')
# game_board[np.where(game_board > 0)] = np.log2(game_board[np.where(game_board > 0)])
# game_board = game_board.reshape(16,)
# # Define C data
# ffi = FFI()
# g_board = ffi.new('uint8_t tmp[16]')
# for i in range(16):
#     g_board[i] = game_board[i]

# for i in range(16):
#     print(g_board[i])
# print('')

# # Play out random oves
# tools2048.lib.roll_out(g_board)

# for i in range(16):
#     print(g_board[i])