import os
import sys
sys.path.append(os.getcwd())
import numpy as np
import tools2048
import anytree as at
from joblib import Parallel, delayed

#TODO fix this board state 0.0 0.0 nan nan
# [[   8    4    2  128]
#  [   2   16   64    2]
#  [2048   32    4    2]
#  [   4    2  256    2]]

#TODO figure out nan thing.  what to do with boards that end the game?
def play_out_par(root, ch_ind, child):
    moves = tools2048.checkValidMoves(child.game_board)
    if moves:
        reward = tools2048.roll_out(child.game_board)
        root.children[ch_ind].reward.append(reward)
        root.children[ch_ind].visits += 1
    else:
        root.children[ch_ind].reward.append(np.nan)
        root.children[ch_ind].visits += 1

# game_board = [[2, 16, 2, 0],
#               [4, 32, 2, 0],
#               [8, 128, 64, 0],
#               [16, 128, 0, 0]]
game_board = [[2, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
game_board = np.array(game_board, dtype='uint16')
env = tools2048.play2048()
env.game_board = game_board

n_moves = 300
done = False
print(env.game_board)
while not done:
    # Create all the next moves
    moves = tools2048.checkValidMoves(env.game_board)

    # If there are valid moves, continue
    if moves:
        # generate all possible board states for the next moves
        root = tools2048.MoveNode('root', 1, env.game_board)
        tools2048.gen_next_level(root)

        # Sample for each of these board states for n_moves times
        move_num = 0
        while move_num < n_moves:
            move_num += len(root.children)
            Parallel(n_jobs=2)(delayed(play_out_par)(root, ch_ind, child) for ch_ind, child in enumerate(root.children))
            # for ch_ind, child in enumerate(root.children):
            #     play_out_par(ch_ind, child)
                # moves = tools2048.checkValidMoves(child.game_board)
                # if moves:
                #     reward = tools2048.roll_out(child.game_board)
                #     root.children[ch_ind].reward.append(reward)
                #     root.children[ch_ind].visits += 1
                #     move_num += 1
                # else:
                #     root.children[ch_ind].reward.append(np.nan)
                #     root.children[ch_ind].visits += 1

        left_reward = []
        right_reward = []
        up_reward = []
        down_reward = []
        for child in root.children:
            if 'left' in child.name:
                left_reward.append(np.nanmean(child.reward) * child.probability)
            if 'right' in child.name:
                right_reward.append(np.nanmean(child.reward) * child.probability)
            if 'up' in child.name:
                up_reward.append(np.nanmean(child.reward) * child.probability)
            if 'down' in child.name:
                down_reward.append(np.nanmean(child.reward) * child.probability)

        left_reward = np.sum(left_reward)
        right_reward = np.sum(right_reward)
        up_reward = np.sum(up_reward)
        down_reward = np.sum(down_reward)

        max_reward = left_reward
        move = 0
        if right_reward > max_reward:
            move = 1
            max_reward = right_reward
        if up_reward > max_reward:
            move = 2
            max_reward = up_reward
        if down_reward > max_reward:
            move = 3
            max_reward = down_reward
        print(left_reward, right_reward, up_reward, down_reward)

        _, _, done, _ = env.step(move)
        env.render()
    # If no valid moves, then done
    else:
        done = True