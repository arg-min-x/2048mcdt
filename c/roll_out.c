#include <stdio.h>
#include <stdlib.h>
#include "lib2048.h"
#include <stdint.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

// Test the tree creation and deletion
int main(void) {

for (int ind = 0;ind<1;ind++){
	uint8_t game_board_orig[16] = { 0, 0, 0, 0,
		                            0, 0, 0, 0,
		                            0, 0, 0, 0,
		                            0, 0, 0, 0};
	uint8_t *move_board,*tmp_board;
	int rand_num = 0;
	int keep_moving = 1;
	int num_moves = 0;

	move_board = add_random_number(game_board_orig);
	// print_game_board(move_board);
	// printf("\n");

	int seed = time(NULL);
	srand(seed+1);
	printf("\n");
	while (keep_moving>0){
		
		// Choose a random move
		rand_num = rand() % 4 + 1;
		printf("%d", rand() % 4 + 1);
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
	}
	// printf("\nYou Lose\n");
}
return 1;
}

