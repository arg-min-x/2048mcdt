import numpy as np
import gym
from gym import spaces
from ._lib2048 import lib
from cffi import FFI
import numpy as np


def get_time():
    lib.get_time()

#TODO Fix the list vs np.array in the moves
class play2048(gym.Env):
    """
    Custom Environment that follows gym interface.
    This is a simple env where the agent must learn to go always left.
    """
    # Because of google colab, we cannot implement the GUI ('human' render mode)
    metadata = {'render.modes': ['console']}
    history = []

    def __init__(self):
        super(play2048, self).__init__()
        self.game_board = np.zeros((4, 4))
        self.game_board = add_random_square(self.game_board)

        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)

        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=16384, shape=(4, 4), dtype=np.uint16)

    def reset(self):
        """
        Important: the observation must be a numpy array
        :return: (np.array)
        """
        game_board = np.zeros((4, 4))
        game_board = add_random_square(game_board)
        self.game_board = game_board
        self.history = []
        return game_board

    def step(self, action):

        old_board = self.game_board.copy()
        if action == 0:
            self.game_board = np.array(move_left(self.game_board))
        elif action == 1:
            self.game_board = np.array(move_right(self.game_board))
        elif action == 2:
            self.game_board = np.array(move_up(self.game_board))
        elif action == 3:
            self.game_board = np.array(move_down(self.game_board))
        else:
            raise ValueError("Received invalid action={} which is not part of the action space".format(action))

        # Are there any valid moves?
        game_board_old = self.game_board.copy()
        tmp_board = np.array(move_left(self.game_board))
        done = False
        if np.array_equal(game_board_old, tmp_board):
            tmp_board = np.array(move_right(self.game_board))
            if np.array_equal(game_board_old, tmp_board):
                tmp_board = np.array(move_up(self.game_board))
                if np.array_equal(game_board_old, tmp_board):
                    tmp_board = np.array(move_down(self.game_board))
                    if np.array_equal(game_board_old, tmp_board):
                        done = True

        if (not done) and (not np.array_equal(self.game_board, old_board)):
            self.game_board = add_random_square(self.game_board)

        # Null reward everywhere except when reaching the goal (left of the grid)
        reward = self.game_board.sum()
        # reward = self.game_board.max()

        # Optionally we can pass additional info, we are not using that for now
        info = {}

        return self.game_board, reward, done, info

    def render(self, mode='console'):
        #         if mode != 'console':
        #           raise NotImplementedError()
        print(self.game_board)

    def close(self):
        pass

def roll_out_c(board):

    # prepare the game board
    game_board = board.copy()
    game_board[np.where(game_board > 0)] = np.log2(game_board[np.where(game_board > 0)])
    game_board = game_board.reshape(16,)

    # Define C data
    ffi = FFI()
    g_board = ffi.new('uint8_t tmp[16]')
    seed = np.random.randint(500000)
    for i in range(16):
        g_board[i] = game_board[i]

    # Play out random oves
    lib.roll_out(g_board, seed)

    # convert back to python and calculate score
    game_board = [g_board[ind] for ind in range(16)]
    game_board = [2**game_board[ind] for ind in range(16)]
    return np.sum(game_board)


# def move_right_c(board):
#     # prepare the game board
#     game_board = board.copy()
#     game_board[np.where(game_board > 0)] = np.log2(game_board[np.where(game_board > 0)])
#     game_board = game_board.reshape(16,)
    
#     # Define C data
#     ffi = FFI()
#     g_board = ffi.new('uint8_t tmp[16]')
#     for i in range(16):
#         g_board[i] = game_board[i]
#     g_board = lib.move_right(g_board)

#     # convert back to python and calculate score
#     game_board = [g_board[ind] for ind in range(16)]
#     game_board = np.array(game_board).reshape(4, 4)
#     game_board[np.where(game_board > 0)] = np.power(2, game_board[np.where(game_board > 0)])
#     return game_board

def move_right_c(board):
    # prepare the game board
    game_board = board.reshape(16,)
    
    # Define C data
    ffi = FFI()
    g_board = ffi.new('uint32_t tmp[16]')
    for i in range(16):
        g_board[i] = game_board[i]
    g_board = lib.move_right32(g_board)

    # convert back to python and calculate score
    game_board = [g_board[ind] for ind in range(16)]
    game_board = np.array(game_board).reshape(4, 4)
    return game_board

# Find all the valid moves
def checkValidMoves(game_board):
    # Generate all game boards after all moves
    left_game_board = move_left(game_board)
    right_game_board = move_right(game_board)
    up_game_board = move_up(game_board)
    down_game_board = move_down(game_board)

    # Store true false in an array 0 = right, 1 = left, 2 = up, 3 = down
    moves = []
    if not np.array_equal(np.array(game_board), np.array(left_game_board)):
        moves.append(0)
    if not np.array_equal(np.array(game_board), np.array(right_game_board)):
        moves.append(1)
    if not np.array_equal(np.array(game_board), np.array(up_game_board)):
        moves.append(2)
    if not np.array_equal(np.array(game_board), np.array(down_game_board)):
        moves.append(3)

    return moves

# Find all the valid moves
def checkValidMoves_new(game_board):
    # Generate all game boards after all moves
    left_game_board = move_left(game_board)
    right_game_board = move_right(game_board)
    up_game_board = move_up(game_board)
    down_game_board = move_down(game_board)

    # Store true false in an array 0 = right, 1 = left, 2 = up, 3 = down
    moves = []
    if not np.array_equal(game_board, left_game_board):
        moves.append(0)
    if not np.array_equal(game_board, right_game_board):
        moves.append(1)
    if not np.array_equal(game_board, up_game_board):
        moves.append(2)
    if not np.array_equal(game_board, down_game_board):
        moves.append(3)

    return moves

def add_random_square(game_board):
    """
    Adds a 2 or four value to a random location on the board
    """
    game_board = np.array(game_board)
    zero_inds = np.where(game_board == 0)

    fill_two = np.random.randint(1, 11)
    if fill_two <= 9:
        fill_val = 2
    else:
        fill_val = 4

    fil_ind = np.random.choice(np.arange(zero_inds[0].shape[0]))
    game_board[zero_inds[0][fil_ind], zero_inds[1][fil_ind]] = fill_val

    return game_board

# Generate all possible game boards from a given board state
def genBoards(game_board):
    zeroInd = np.where(np.array(game_board) == 0)
    num_boards = len(zeroInd[0])
    game_board = np.array(game_board)
    boards = []

    # All boards with a 2  and added
    for ind in range(0, num_boards):
        tmp = game_board.copy()
        tmp[zeroInd[0][ind], zeroInd[1][ind]] = 2
        boards.append(tmp)
    for ind in range(0, num_boards):
        tmp = game_board.copy()
        tmp[zeroInd[0][ind], zeroInd[1][ind]] = 4
        boards.append(tmp)

    return boards

# -------------------------- Function for calculating down move --------------------------
def move_down(game_board):
    # Create the 2D array to store the board
    new_game_board = [[0 for x in range(4)] for x in range(4)]

    # Move the rows down
    for col_ind in range(0, 4):

        temp_ind = 3

        for row_ind in range(3, -1, -1):

            if game_board[row_ind][col_ind] != 0:
                new_game_board[temp_ind][col_ind] = game_board[row_ind][col_ind]
                temp_ind = temp_ind - 1

    # Combine like blocks
    for col_ind in range(0, 4):

        row_ind_cond = 3

        while row_ind_cond != 0:

            if new_game_board[row_ind_cond][col_ind] == new_game_board[row_ind_cond - 1][col_ind]:

                new_game_board[row_ind_cond][col_ind] = 2 * new_game_board[row_ind_cond - 1][col_ind]

                for row_ind in range(row_ind_cond - 1, 0, -1):
                    new_game_board[row_ind][col_ind] = new_game_board[row_ind - 1][col_ind]

                new_game_board[0][col_ind] = 0

            row_ind_cond = row_ind_cond - 1

    return new_game_board


# -------------------------- Function for calculating right move --------------------------
def move_right(game_board):

    # Create the 2D array to store the board
    new_game_board = [[0 for x in range(4)] for x in range(4)]

    # Move the rows down
    for col_ind in range(0, 4):

        temp_ind = 3

        for row_ind in range(3, -1, -1):

            if game_board[col_ind][row_ind] != 0:
                new_game_board[col_ind][temp_ind] = game_board[col_ind][row_ind]
                temp_ind = temp_ind - 1

    # Combine like blocks
    for col_ind in range(0, 4):

        row_ind_cond = 3

        while row_ind_cond != 0:

            if new_game_board[col_ind][row_ind_cond] == new_game_board[col_ind][row_ind_cond - 1]:

                new_game_board[col_ind][row_ind_cond] = 2 * new_game_board[col_ind][row_ind_cond - 1]

                for row_ind in range(row_ind_cond - 1, 0, -1):
                    new_game_board[col_ind][row_ind] = new_game_board[col_ind][row_ind - 1]

                new_game_board[col_ind][0] = 0

            row_ind_cond = row_ind_cond - 1

    return new_game_board


# -------------------------- Function for calculating up move --------------------------
def move_up(game_board):

    # Create the 2D array to store the board
    new_game_board = [[0 for x in range(4)] for x in range(4)]

    # Move the rows down
    for col_ind in range(0, 4):

        temp_ind = 0

        for row_ind in range(0, 4):

            if game_board[row_ind][col_ind] != 0:
                new_game_board[temp_ind][col_ind] = game_board[row_ind][col_ind]
                temp_ind = temp_ind + 1

    # Combine like blocks
    for col_ind in range(0, 4):

        row_ind_cond = 0

        while row_ind_cond != 3:

            if new_game_board[row_ind_cond][col_ind] == new_game_board[row_ind_cond + 1][col_ind]:

                new_game_board[row_ind_cond][col_ind] = 2 * new_game_board[row_ind_cond + 1][col_ind]

                for row_ind in range(row_ind_cond + 1, 3):
                    new_game_board[row_ind][col_ind] = new_game_board[row_ind + 1][col_ind]

                new_game_board[3][col_ind] = 0

            row_ind_cond = row_ind_cond + 1

    return new_game_board


# -------------------------- Function for calculating left move --------------------------
def move_left(game_board):

    # Create the 2D array to store the board
    new_game_board = [[0 for x in range(4)] for x in range(4)]

    # Move the rows down
    for col_ind in range(0, 4):

        temp_ind = 0

        for row_ind in range(0, 4):

            if game_board[col_ind][row_ind] != 0:
                new_game_board[col_ind][temp_ind] = game_board[col_ind][row_ind]
                temp_ind = temp_ind + 1

    # Combine like blocks
    for col_ind in range(0, 4):

        row_ind_cond = 0

        while row_ind_cond != 3:

            if new_game_board[col_ind][row_ind_cond] == new_game_board[col_ind][row_ind_cond + 1]:

                new_game_board[col_ind][row_ind_cond] = 2 * new_game_board[col_ind][row_ind_cond + 1]

                for row_ind in range(row_ind_cond + 1, 3):
                    new_game_board[col_ind][row_ind] = new_game_board[col_ind][row_ind + 1]

                new_game_board[col_ind][3] = 0

            row_ind_cond = row_ind_cond + 1

    return new_game_board
