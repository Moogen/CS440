import numpy as np

def print_moves(moves):
	is_white_turn = True
	for move in moves:
		start, end = move
		if is_white_turn:
			print("White: " + str(start) + " to " + str(end))
		else:
			print("Black: " + str(start) + " to " + str(end))
		is_white_turn = not is_white_turn