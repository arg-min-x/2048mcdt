//
//  lib2048.c
//  2048-AI
//
//  Created by Adam Rich on 4/11/16.
//  Copyright © 2016 Adam Rich. All rights reserved.
//

#include "lib2048.h"
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <omp.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>


// ========================================================================================
//          Game Board Manipulation
// ========================================================================================

void print_game_board(uint8_t *game_board){
    for (int ind = 0; ind < 4; ind++) {
        printf("%d\t%d\t%d\t%d\n",game_board[0+4*ind],game_board[1+4*ind],game_board[2+4*ind]
               ,game_board[3+4*ind]);
    }
}

// ========================================================================================
// Move Right
uint8_t *move_right(uint8_t *game_board){
    
    // Allocate the new board and copy the old board into it
    uint8_t *move_board = malloc(16*sizeof(uint8_t));
    for (int ind = 0; ind<16; ind++) {
        move_board[ind] = game_board[ind];
    }
    
    for (int repeat = 0; repeat < 3; repeat++) {
        // Shift out zeros
        for (int offset = 0; offset<13; offset +=4) {
            for (int ind = 3; ind >0; ind--) {
                
                // If The current value is zero
                if (move_board[ind+offset] == 0) {
                    // shift value
                    move_board[ind+offset] = move_board[ind+offset-1];
                    move_board[ind-1+offset] = 0;
                }
            }
        }
    }
    
    // Combine like blocks and shift
    for (int offset = 0; offset<13; offset +=4) {
        for (int ind = 3; ind >0; ind--) {
            
            // if the two adjecent values are equal
            if (move_board[ind+offset] == move_board[ind-1+offset] && move_board[ind+offset]>0) {
                move_board[ind+offset] = move_board[ind+offset] + 1;
                move_board[ind-1+offset] = 0;
            }
        }
    }

    // Shift out zeros
    for (int offset = 0; offset<13; offset +=4) {
        for (int ind = 3; ind >0; ind--) {
            
            // If The current value is zero
            if (move_board[ind+offset] == 0) {
                // shift value
                move_board[ind+offset] = move_board[ind+offset-1];
                move_board[ind-1+offset] = 0;
            }
        }
    }
    
    return move_board;
}

// ========================================================================================
// Move the Game Board left
uint8_t *move_left(uint8_t *game_board){
    
    uint8_t *move_board = malloc(16*sizeof(uint8_t));
    for (int ind = 0; ind<16; ind++) {
        move_board[ind] = game_board[ind];
    }
    
    // Shift out zeros
    for (int repeat = 0; repeat<3; repeat++) {
        for (int offset = 0; offset<13; offset +=4) {
            for (int ind = 0; ind < 3; ind++) {
                
                // If The current value is zero
                if (move_board[ind+offset] == 0) {
                    // shift value
                    move_board[ind+offset] = move_board[ind+offset+1];
                    move_board[ind+1+offset] = 0;
                }
            }
        }
    }
    
    // Combine like blocks and shift
    for (int offset = 0; offset<13; offset +=4) {
        for (int ind = 0; ind < 3; ind++) {
            
            // if the two adjecent values are equal
            if (move_board[ind+offset] == move_board[ind+1+offset] && move_board[ind+offset]>0) {
                move_board[ind+offset] +=1;
                move_board[ind+1+offset] = 0;
            }
        }
    }
    
    // Shift out zeros
    for (int offset = 0; offset<13; offset +=4) {
        for (int ind = 0; ind < 3; ind++) {
            
            // If The current value is zero
            if (move_board[ind+offset] == 0) {
                
                // shift value
                move_board[ind+offset] = move_board[ind+offset+1];
                move_board[ind+1+offset] = 0;
            }
        }
    }
    return move_board;
}

// ========================================================================================
// Move the Game Board up
uint8_t *move_up(uint8_t *game_board){
    
    uint8_t *move_board = malloc(16*sizeof(uint8_t));
    for (int ind = 0; ind<16; ind++) {
        move_board[ind] = game_board[ind];
    }
    
    // Shift out zeros
    for (int repeat = 0; repeat<4; repeat++) {
        for (int offset = 0; offset<4; offset ++) {
            for (int ind = 0; ind < 12; ind+=4) {
                
                // If The current value is zero
                if (move_board[ind+offset] == 0) {
                    // shift value
                    move_board[ind+offset] = move_board[ind+offset+4];
                    move_board[ind+4+offset] = 0;
                }
            }
        }
    }
    
    // Combine like blocks and shift
    for (int offset = 0; offset<4; offset ++) {
        for (int ind = 0; ind < 12; ind+=4) {
            
            // if the two adjecent values are equal
            if (move_board[ind+offset] == move_board[ind+4+offset] && move_board[ind+offset]>0) {
                move_board[ind+offset] +=1;
                move_board[ind+4+offset] = 0;
            }
        }
    }

    // Shift out zeros
    for (int repeat = 0; repeat<2; repeat++) {
        for (int offset = 0; offset<4; offset ++) {
            for (int ind = 0; ind < 12; ind+=4) {
                
                // If The current value is zero
                if (move_board[ind+offset] == 0) {
                    // shift value
                    move_board[ind+offset] = move_board[ind+offset+4];
                    move_board[ind+4+offset] = 0;
                }
            }
        }
    }
    return move_board;
}

// ========================================================================================
// Move the Game Board down
uint8_t *move_down(uint8_t *game_board){
    
    uint8_t *move_board = malloc(16*sizeof(uint8_t));
    for (int ind = 0; ind<16; ind++) {
        move_board[ind] = game_board[ind];
    }
    
    // Shift out zeros
    for (int repeat = 0; repeat<4; repeat++) {
        for (int offset = 0; offset<4; offset ++) {
            for (int ind = 12; ind > 3 ; ind-=4) {
                
                // If The current value is zero
                if (move_board[ind+offset] == 0) {
                    // shift value
                    move_board[ind+offset] = move_board[ind+offset-4];
                    move_board[ind-4+offset] = 0;
                }
            }
        }
    }
    
    // Combine like blocks and shift
    for (int offset = 0; offset<4; offset ++) {
        for (int ind = 12; ind > 3 ; ind-=4) {
            
            // if the two adjecent values are equal
            if (move_board[ind+offset] == move_board[ind-4+offset] && move_board[ind+offset]>0) {
                move_board[ind+offset] +=1;
                move_board[ind-4+offset] = 0;
            }
        }
    }
    
    // Shift out zeros
    for (int repeat = 0; repeat<2; repeat++) {
        for (int offset = 0; offset<4; offset ++) {
            for (int ind = 12; ind > 3 ; ind-=4) {
                
                // If The current value is zero
                if (move_board[ind+offset] == 0) {
                    // shift value
                    move_board[ind+offset] = move_board[ind+offset-4];
                    move_board[ind-4+offset] = 0;
                }
            }
        }
    }
    return move_board;
}

// ========================================================================================
// Count the number of zeros on the board
uint8_t count_zeros(uint8_t *game_board){
    uint8_t zero_count = 0;
    
    for (int ind =0; ind<16; ind++) {
        if (game_board[ind]==0) {
            zero_count++;
        }
    }
    return zero_count;
}

// Compare to boards return 1 if they are the same
uint8_t compare_board(uint8_t *board1, uint8_t *board2){
	int identical = 1;
	for (int ind = 0; ind<16; ind++){
		if (board1[ind] != board2[ind]){
			identical = 0;
		}
	}
return identical;
}

// ========================================================================================
// Create a board with two or four added at a zero locations
uint8_t *create_random_board(uint8_t *game_board, int *last_zero_ind, uint8_t rand_value){
    int ind;
    uint8_t *rand_board = malloc(16*sizeof(uint8_t));
    for (int ind = 0; ind<16; ind++) {
        rand_board[ind] = game_board[ind];
    }
    
    for (ind = *last_zero_ind; ind<16; ind++) {
        if (rand_board[ind]==0) {
            rand_board[ind] = rand_value;
            break;
        }
    }
    *last_zero_ind = ind+1;
    return rand_board;
}

// ========================================================================================
// adds a 2 or 4 to the board in a random location
uint8_t *add_random_number(uint8_t *game_board){
    int num_zeros, ind_z, rand_ind, rand_num;
	ind_z = 0;
	num_zeros = count_zeros(game_board);
	int *zero_inds;
	zero_inds = malloc(sizeof(int)*num_zeros);

	for (int ind =0; ind<16; ind++){
		if (game_board[ind] ==0) {
			zero_inds[ind_z] = ind;
			ind_z++;
		}	
	}
	
	rand_ind = rand() % num_zeros + 0;
	rand_num = rand() % 100 + 1;
	if (rand_num <11){
		rand_num = 2;
	}else{
		rand_num = 1;
	}

	game_board[zero_inds[rand_ind]] = rand_num;
	//printf("\n rand ind %d  zero ind %d rand num %d\n",rand_ind, zero_inds[rand_ind], rand_num);

	
	//for (int ind = 0; ind<num_zeros; ind++){
	//	printf("%d ",zero_inds[ind]);	
	//}
	free(zero_inds);
    return game_board;
}

// Test the tree creation and deletion
void roll_out(uint8_t *game_board, int seed) {

    srand(seed);
	uint8_t *tmp_board;
	int rand_num = 0;
	int keep_moving = 1;
	int num_moves = 0;

    uint8_t *move_board = malloc(16*sizeof(uint8_t));
    for (int ind = 0;ind<16;ind++){
        move_board[ind] = game_board[ind];
    }
	// move_board = add_random_number(game_board_orig);
 //    print_game_board(game_board);
 //    printf("\n");
	// print_game_board(move_board);
	// printf("\n");

	while (keep_moving>0){
		// Choose a random move
		rand_num = rand() % 4 + 1;
		char next_move = 'a';
		char up, down, left, right;
		up = 'u';
		down = 'd';
		left = 'l';
		right = 'r';
		if (rand_num==1){
			next_move = up;
		}else if (rand_num==2){
			next_move = down;
		}else if (rand_num ==3){
			next_move = left;
		}else if (rand_num ==4){
			next_move = right;
		}

		tmp_board = move_up(move_board);
		if (next_move==up && !compare_board(tmp_board,move_board)){
			move_board = move_up(move_board);
			move_board = add_random_number(move_board);
			// print_game_board(move_board);
			// printf("\n");
			num_moves++;
		}
		tmp_board = move_down(move_board);
		if(next_move==down && !compare_board(tmp_board,move_board)){
			move_board = move_down(move_board);
			move_board = add_random_number(move_board);
			// print_game_board(move_board);
			// printf("\n");
			num_moves++;
		}
		tmp_board = move_left(move_board);
		if(next_move==left && !compare_board(tmp_board,move_board)){
			move_board = move_left(move_board);
			move_board = add_random_number(move_board);
			// print_game_board(move_board);
			// printf("\n");
			num_moves++;
		}
		tmp_board = move_right(move_board);
		if(next_move==right && !compare_board(tmp_board,move_board)){
			move_board = move_right(move_board);
			move_board = add_random_number(move_board);
			// print_game_board(move_board);
			// printf("\n");
			num_moves++;
		}

		// If all the moves result in an identical board state
		tmp_board = move_left(move_board);
		if (compare_board(tmp_board,move_board)){
			tmp_board = move_right(move_board);
			if (compare_board(tmp_board,move_board)){
				tmp_board = move_up(move_board);
				if (compare_board(tmp_board,move_board)){
					tmp_board = move_down(move_board);
					if (compare_board(tmp_board,move_board)){
						keep_moving = 0;
					}
				}
			}
		}
		// printf("\nYou Lose\n");
	for (int ind = 0;ind<16;ind++){
		game_board[ind] = move_board[ind];
	}
	// print_game_board(game_board);
	}
    free(move_board);
}