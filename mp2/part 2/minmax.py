from board import setup, get_moves, make_move, winner_exists, print_board
from print_utils import print_moves
import random
import numpy as np
import time

max_depth = 2
num_simulations = 10
num_wins_white = 0
num_wins_black = 0
average_total_nodes = 0
average_black_nodes = 0
average_white_nodes = 0

#global resettable vars
best_move = None
total_nodes = 0
black_nodes = 0
white_nodes = 0
is_white_turn_global = True

white_heuristic = None
black_heuristic = None

def reset():
	global best_move, total_nodes, black_nodes, white_nodes
	best_move = None
	total_nodes = 0
	black_nodes = 0
	white_nodes = 0

def minmax_vs_alphabeta():
	global best_move, white_heuristic, black_heuristic

	#change these heuristics depending on which problem you're doing
	white_heuristic = dummy_heuristic_offensive
	black_heuristic = dummy_heuristic_offensive

	white_workers, black_workers = setup()
	winner = False
	is_white_turn = True
	moves = np.array(np.zeros((0, 2, 2)))
	while(not winner):
		best_move = None
		if is_white_turn:
			utility = minmax(white_workers, black_workers, 0, is_white_turn)
		else:
			utility = alpha_beta(white_workers, black_workers, 0, is_white_turn, -99999, -99999)
		
		#make the move
		white_workers, black_workers = make_move(white_workers, black_workers, is_white_turn, best_move)
		winner, utility, name = winner_exists(white_workers, black_workers)
		moves = np.insert(moves, len(moves), best_move, 0)

		is_white_turn = not is_white_turn
		
	print_board(white_workers, black_workers)
	print(total_nodes, black_nodes, white_nodes)

def run_alphabeta():
	global best_move, white_heuristic, black_heuristic, is_white_turn_global
	global average_total_nodes, average_white_nodes, average_black_nodes, num_wins_white, num_wins_black

	start_time = time.time()

	#change these heuristics depending on which problem you're doing
	white_heuristic = dummy_heuristic_offensive
	black_heuristic = dummy_heuristic_defensive

	#run boardgame matches a certain number of times
	for i in range(num_simulations):
		reset()

		white_workers, black_workers = setup()
		winner = False
		is_white_turn_global = True
		moves = np.array(np.zeros((0, 2, 2)))

		while(not winner):
			best_move = None
			utility = alpha_beta(white_workers, black_workers, 0, is_white_turn_global, -99999, -99999)
			#utility = minmax(white_workers, black_workers, 0, is_white_turn_global)
			
			#make the move
			white_workers, black_workers = make_move(white_workers, black_workers, is_white_turn_global, best_move)
			winner, utility, winner_name = winner_exists(white_workers, black_workers)
			moves = np.insert(moves, len(moves), best_move, 0)

			is_white_turn_global = not is_white_turn_global
			
		print_board(white_workers, black_workers)
		print(total_nodes, black_nodes, white_nodes)

		#update simulation variables
		if winner_name == 'white':
			num_wins_white += 1
		elif winner_name == 'black':
			num_wins_black += 1

		average_total_nodes += total_nodes
		average_black_nodes += black_nodes
		average_white_nodes += white_nodes

	average_total_nodes /= num_simulations
	average_black_nodes /= num_simulations
	average_white_nodes /= num_simulations
	print("White wins: " + str(num_wins_white), "Black wins: " + str(num_wins_black))
	print("Average total nodes: " + str(average_total_nodes))
	print("Average black nodes: " + str(average_black_nodes))
	print("Average white nodes: " + str(average_white_nodes))

	end_time = time.time()
	print("Time: " + str(end_time - start_time))

def minmax(white_workers, black_workers, depth, is_white_turn):
	'''[summary]
	
	[description]
	
	Arguments:
		white_workers {[type]} -- [description]
		black_workers {[type]} -- [description]
		depth {[type]} -- [description]
	
	Returns:
		float -- utility value
	'''
	global best_move, total_nodes, black_nodes, white_nodes, white_heuristic, black_heuristic, is_white_turn_global

	total_nodes += 1
	if is_white_turn:
		white_nodes += 1
	else:
		black_nodes += 1
	winner, utility, name = winner_exists(white_workers, black_workers)
	#check for winner first
	if winner:
		return utility
	#then do a depth check
	if depth >= max_depth:
		if is_white_turn_global:
			utility = white_heuristic(white_workers, black_workers, is_white_turn_global)
		else:
			utility = black_heuristic(white_workers, black_workers, is_white_turn_global)
		return utility

	moves = get_moves(white_workers, black_workers, is_white_turn)
	utility = -99999
	for move in moves:
		new_white_workers, new_black_workers = make_move(white_workers, black_workers, is_white_turn, move)
		result = minmax(new_white_workers, new_black_workers, depth + 1, not is_white_turn)
		if utility < result:
			utility = result
			if (depth == 0): 
				best_move = np.copy(move)

	return utility

def alpha_beta(white_workers, black_workers, depth, is_white_turn, alpha, beta):
	global best_move, total_nodes, black_nodes, white_nodes, white_heuristic, black_heuristic, is_white_turn_global

	total_nodes += 1
	if is_white_turn:
		white_nodes += 1
	else:
		black_nodes += 1
	winner, utility, name = winner_exists(white_workers, black_workers)
	#check for winner first
	if winner:
		return utility
	#then do a depth check
	if depth >= max_depth:
		if is_white_turn_global:
			utility = white_heuristic(white_workers, black_workers, is_white_turn_global)
		else:
			utility = black_heuristic(white_workers, black_workers, is_white_turn_global)
		return utility

	moves = get_moves(white_workers, black_workers, is_white_turn)
	utility = -99999
	for move in moves:
		new_white_workers, new_black_workers = make_move(white_workers, black_workers, is_white_turn, move)
		result = alpha_beta(new_white_workers, new_black_workers, depth + 1, not is_white_turn, alpha, beta)
		if utility < result:
			utility = result
			if (depth == 0): 
				best_move = np.copy(move)
		if is_white_turn:
			if result < beta:
				return utility
			alpha = max(alpha, utility)
		else:
			if result < alpha:
				return utility
			beta = max(beta, utility)

	return utility

def dummy_heuristic_offensive(white_workers, black_workers, is_white_turn):
	if is_white_turn:
		return 2 * (30 - len(black_workers)) + random.random()
	else:
		return 2 * (30 - len(white_workers)) + random.random()

def dummy_heuristic_defensive(white_workers, black_workers, is_white_turn):
	if is_white_turn:
		return 2 * len(white_workers) + random.random()
	else:
		return 2 * len(black_workers) + random.random()

def smart_heuristic_offensive(white_workers, black_workers, is_white_turn):
	if is_white_turn:
		return np.sum(white_workers[:,1:]) - np.sum(black_workers[:, 1:])
	else:
		return np.sum(black_workers[:,1:]) - np.sum(white_workers[:, 1:])


#minmax_vs_alphabeta()
run_alphabeta()