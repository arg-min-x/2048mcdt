import os
import sys
sys.path.append(os.getcwd())
import numpy as np
import tools2048
import anytree as at
from joblib import Parallel, delayed


def play_out_par(child):
    moves = tools2048.checkValidMoves(child.game_board)
    if moves:
        reward = tools2048.roll_out_c(child.game_board)
    else:
        reward = np.nan
    return reward

game_board = [[2, 16, 2, 0],
              [4, 32, 2, 0],
              [8, 128, 64, 0],
              [16, 128, 0, 0]]
def main():
    game_board = [[2, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
    game_board = np.array(game_board, dtype='uint16')
    env = tools2048.play2048()
    env.game_board = game_board

    n_moves = 2000
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
                # Sample for each of these board states for n_moves times
                # reward = Parallel(n_jobs=2)(delayed(play_out_par)(child) for child in root.children)
                reward = [play_out_par(child) for child in root.children]
                # print(reward)
                for ch_ind, child in enumerate(root.children):
                    moves = tools2048.checkValidMoves(child.game_board)
                    if moves:
                        root.children[ch_ind].reward.append(reward[ch_ind])
                        root.children[ch_ind].visits += 1
                    else:
                        root.children[ch_ind].reward.append(np.nan)
                        root.children[ch_ind].visits += 1

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

            left_reward = np.nansum(left_reward)
            right_reward = np.nansum(right_reward)
            up_reward = np.nansum(up_reward)
            down_reward = np.nansum(down_reward)

            r_list = [left_reward, right_reward, up_reward, down_reward]
            print(r_list)
            if np.nanmax(r_list) > 0:
                move = np.nanargmax(r_list)
                _, _, done, _ = env.step(move)
                env.render()
            else:
                done = True
            if done == True:
                breakpoint()
            
        # If no valid moves, then done
        else:
            done = True
    env.render()
if __name__ == '__main__':
    main()
# game_board = [[2, 0, 0, 0],
#               [0, 0, 0, 0],
#               [0, 0, 0, 0],
#               [0, 0, 0, 0]]
# game_board = np.array(game_board, dtype='uint16')
# env = tools2048.play2048()
# env.game_board = game_board
#
# moves = tools2048.checkValidMoves(env.game_board)
#
# # generate all possible board states for the next moves
# root = tools2048.MoveNode('root', 1, env.game_board)
# tools2048.gen_next_level(root)
#
# # Sample for each of these board states for n_moves times
# reward = Parallel(n_jobs=2)(delayed(play_out_par)(child) for child in root.children)
# print(reward)
# for ch_ind, child in enumerate(root.children):
#     moves = tools2048.checkValidMoves(child.game_board)
#     if moves:
#         root.children[ch_ind].reward.append(reward[ch_ind])
#         root.children[ch_ind].visits += 1
#     else:
#         root.children[ch_ind].reward.append(np.nan)
#         root.children[ch_ind].visits += 1