import tools2048
import numpy as np

game_board = [[0, 2, 2, 4],
              [4, 8, 2, 2],
              [2, 4, 8, 4],
              [4, 4, 2, 0]]
for ind in range(100):
    tmp = tools2048.roll_out_c(game_board)
