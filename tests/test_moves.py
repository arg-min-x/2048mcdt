import pytest
import numpy as np
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
sys.path.append(os.path.abspath(os.getcwd()))
import tools2048

@pytest.mark.parametrize("in_board, out_board",
                         [
                             ([[2, 2, 2, 0],
                              [2, 0, 2, 2],
                              [0, 2, 0, 2],
                              [0, 0, 2, 0]],
                             [[4, 4, 4, 4],
                              [0, 0, 2, 0],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]]),
                             ([[2, 2, 2, 0],
                               [2, 16, 2, 2],
                               [2, 2, 4, 0],
                               [2, 0, 4, 2]],
                              [[4, 2, 4, 4],
                               [4, 16, 8, 0],
                               [0, 2, 0, 0],
                               [0, 0, 0, 0]])
                         ]
                         )
def test_up_move(in_board, out_board):
    test_board = tools2048.move_up(np.array(in_board))
    assert np.array_equal(test_board, np.array(out_board))

@pytest.mark.parametrize("in_board, out_board",
                         [
                             ([[2, 2, 2, 0],
                              [2, 0, 2, 2],
                              [0, 2, 0, 2],
                              [0, 0, 2, 0]],
                             [[0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 0, 2, 0],
                              [4, 4, 4, 4]]),
                             ([[2, 2, 2, 0],
                               [2, 16, 2, 2],
                               [2, 2, 4, 0],
                               [2, 0, 4, 2]],
                              [[0, 0, 0, 0],
                               [0, 2, 0, 0],
                               [4, 16, 4, 0],
                               [4, 2, 8, 4]])
                         ]
                         )
def test_up_down(in_board, out_board):
    test_board = tools2048.move_down(np.array(in_board))
    assert np.array_equal(test_board, np.array(out_board))

@pytest.mark.parametrize("in_board, out_board",
                         [
                             ([[2, 2, 2, 0],
                              [2, 0, 2, 2],
                              [0, 2, 0, 2],
                              [0, 0, 2, 0]],
                             [[4, 2, 0, 0],
                              [4, 2, 0, 0],
                              [4, 0, 0, 0],
                              [2, 0, 0, 0]]),
                             ([[2, 2, 2, 0],
                               [2, 16, 2, 2],
                               [2, 2, 4, 0],
                               [2, 0, 4, 2]],
                              [[4, 2, 0, 0],
                               [2, 16, 4, 0],
                               [4, 4, 0, 0],
                               [2, 4, 2, 0]])
                         ]
                         )
def test_up_left(in_board, out_board):
    test_board = tools2048.move_left(np.array(in_board))
    assert np.array_equal(test_board, np.array(out_board))

@pytest.mark.parametrize("in_board, out_board",
                         [
                             ([[2, 2, 2, 0],
                              [2, 0, 2, 2],
                              [0, 2, 0, 2],
                              [0, 0, 2, 0]],
                             [[0, 0, 2, 4],
                              [0, 0, 2, 4],
                              [0, 0, 0, 4],
                              [0, 0, 0, 2]]),
                             ([[2, 2, 2, 0],
                               [2, 16, 2, 2],
                               [2, 2, 4, 0],
                               [2, 0, 4, 2]],
                              [[0, 0, 2, 4],
                               [0, 2, 16, 4],
                               [0, 0, 4, 4],
                               [0, 2, 4, 2]])
                         ]
                         )
def test_up_right(in_board, out_board):
    test_board = tools2048.move_right(np.array(in_board))
    assert np.array_equal(test_board, np.array(out_board))
    
@pytest.mark.parametrize("in_board, out_board",
                         [
                             ([[2, 2, 2, 0],
                              [2, 0, 2, 2],
                              [0, 2, 0, 2],
                              [0, 0, 2, 0]],
                             [[0, 0, 2, 4],
                              [0, 0, 2, 4],
                              [0, 0, 0, 4],
                              [0, 0, 0, 2]]),
                             ([[2, 2, 2, 0],
                               [2, 16, 2, 2],
                               [2, 2, 4, 0],
                               [2, 0, 4, 2]],
                              [[0, 0, 2, 4],
                               [0, 2, 16, 4],
                               [0, 0, 4, 4],
                               [0, 2, 4, 2]])
                         ]
                         )
def test_up_right_c(in_board, out_board):
    test_board = tools2048.move_right_c(np.array(in_board))
    assert np.array_equal(test_board, np.array(out_board))