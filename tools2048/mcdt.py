import numpy as np
import anytree as at
from .gameboard import *

class MoveNode(at.NodeMixin):
    def __init__(self, name, probability, game_board, parent=None, children=None):
        self.probability = probability
        self.name = name
        self.parent = parent
        self.game_board = game_board
        self.visits = 0
        self.reward = []
        if children:
            self.children = children

    def __repr__(self):
        if self.parent:
            return(self.parent.__repr__() + '/' + self.name)
        else:
            return(self.name)


def roll_out(game_board):
    env = play2048()
    env.game_board = game_board
    done = False
    reward = 0
    while not done:
        moves = checkValidMoves(env.game_board)
        if moves:
            move = np.random.choice(moves)
            _, reward, done, _ = env.step(move)
        else:
            done = True
    return reward

def roll_out_new(game_board):
    done = False
    reward = 0
    while not done:
        moves = checkValidMoves(game_board)
        if moves:
            move = np.random.choice(moves)
            if move == 0:
                game_board = move_left(game_board)
            elif move == 1:
                game_board = move_right(game_board)
            elif move == 2:
                game_board = move_up(game_board)
            elif move == 3:
                game_board = move_down(game_board)
            
            game_board = add_random_square(game_board)
                
        else:
            done = True
            reward = np.sum(game_board)
    return reward

def gen_next_level(root):
    """
    Creates the children of the root node

    Parameters
    ----------
    root : tools2048.MoveNode
        The root node

    Returns
    -------

    """
    game_board = root.game_board.copy()

    # Create boards for left, right, up, down moves
    left_valid = True
    right_valid = True
    up_valid = True
    down_valid = True
    left_board = move_left(game_board)
    if np.array_equal(game_board, left_board):
        left_valid = False
    
    right_board = move_right(game_board)
    if np.array_equal(game_board, right_board):
        right_valid = False
    
    up_board = move_up(game_board)
    if np.array_equal(game_board, up_board):
        up_valid = False
    
    down_board = move_down(game_board)
    if np.array_equal(game_board, down_board):
        down_valid = False
    
    if left_valid:
        gens = genBoards(left_board)
        for ind, board in enumerate(gens):
            if ind < len(gens) / 2:
                p = 2*0.9/len(gens)
            else:
                p = 2*0.1/len(gens)
            MoveNode('left' + str(ind), p, board, parent=root)
    
    if right_valid:
        gens = genBoards(right_board)
        for ind, board in enumerate(gens):
            if ind < len(gens) / 2:
                p = 2*0.9 / len(gens)
            else:
                p = 2*0.1 / len(gens)
            MoveNode('right' + str(ind), p, board, parent=root)
    
    if up_valid:
        gens = genBoards(up_board)
        for ind, board in enumerate(gens):
            if ind < len(gens) / 2:
                p = 2*0.9/len(gens)
            else:
                p = 2*0.1/len(gens)
            MoveNode('up' + str(ind), p, board, parent=root)

    if down_valid:
        gens = genBoards(down_board)
        for ind, board in enumerate(gens):
            if ind < len(gens) / 2:
                p = 2*0.9/len(gens)
            else:
                p = 2*0.1/len(gens)
            MoveNode('down' + str(ind), p, board, parent=root)
