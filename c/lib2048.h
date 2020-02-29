//
//  lib2048.h
//  2048-AI
//
//  Created by Adam Rich on 4/11/16.
//  Copyright © 2016 Adam Rich. All rights reserved.
//

#ifndef lib2048_h
#define lib2048_h

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
// ========================================================================================
//          Game Tree Structures and functions
// ========================================================================================


// ========================================================================================
//          Game Board Manipulation
// ========================================================================================

uint32_t get_time(void);

// Print the game board
void print_game_board(uint8_t *game_board);

//// Print the game board
//void print_game_board_pow_2(uint8_t *game_board);

// Move the game board left return pointer to new board
uint8_t *move_left(uint8_t *game_board);

// Move the game board right and return pointer to the new board
uint8_t *move_right(uint8_t *game_board);
uint32_t *move_right32(uint32_t *game_bard);

// Move the game board up and return pointer to the new board
uint8_t *move_up(uint8_t *game_board);

// Move the game board down and return pointer to the new board
uint8_t *move_down(uint8_t *game_board);

// Count the number of zeros on the board
uint8_t count_zeros(uint8_t *game_board);

// adds a 2 or 4 to the board in a random location
uint8_t *add_random_number(uint8_t *game_board, int seed);

// Create a board with two or four added at a zero locations
uint8_t *create_random_board(uint8_t *game_board, int *last_zero_ind, uint8_t rand_value);

// Compare to boards return 1 if they are the same
uint8_t compare_board(uint8_t *board1, uint8_t *board2);

//
void roll_out(uint8_t *game_board, int seed);
#endif /* lib2048_h */
