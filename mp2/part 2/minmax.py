from board import setup, get_moves, make_move, winner_exists, print_board
from print_utils import print_moves
import random
import numpy as np
import time

max_depth = 3 #max depth of the search three
num_simulations = 10 #number of times to run the breakthrough game
num_wins_white = 0
num_wins_black = 0

#global resettable vars
best_move = None
is_white_turn_global = True

#global printing variables
total_nodes = 0
black_nodes = 0
white_nodes = 0
average_total_nodes = 0
average_time_per_move = 0

white_heuristic = None
black_heuristic = None

def reset():
	global best_move, total_nodes, black_nodes, white_nodes
	best_move = None

def run_alphabeta():
	global best_move, white_heuristic, black_heuristic, is_white_turn_global, average_total_nodes, average_time_per_move
	global num_wins_white, num_wins_black

	start_time = time.time()

	#change these heuristics depending on which problem you're doing
	white_heuristic = custom_heuristic_offensive
	black_heuristic = custom_heuristic_defensive

	#run boardgame matches a certain number of times
	for i in range(num_simulations):
		reset()

		white_workers, black_workers = setup()
		winner = False
		is_white_turn_global = True
		moves = np.array(np.zeros((0, 2, 2)))

		game_time = time.time()

		while(not winner):
			best_move = None
			#print(utility, is_white_turn_global)
			utility = alpha_beta(white_workers, black_workers, 0, is_white_turn_global, -99999, -99999)
			
			#make the move
			white_workers, black_workers = make_move(white_workers, black_workers, is_white_turn_global, best_move)
			winner, utility, winner_name = winner_exists(white_workers, black_workers)
			moves = np.insert(moves, len(moves), best_move, 0)

			is_white_turn_global = not is_white_turn_global
			#print_board(white_workers, black_workers)

		average_time_per_move += (time.time() - game_time) / len(moves)
		#The final state of the board (who owns each square) and the winning player.
		print_board(white_workers, black_workers)
		print("Winner: " + winner_name)
		print()

		#The number of opponent workers captured by each player, as well as the total number of moves required till the win.
		print("Pieces captured by white: " + str(16 - len(black_workers)))
		print("Pieces captured by black: " + str(16 - len(white_workers)))
		print("Number of moves: " + str(len(moves)))

		#update simulation variables
		if winner_name == 'white':
			num_wins_white += 1
		elif winner_name == 'black':
			num_wins_black += 1
		average_total_nodes += total_nodes / len(moves)

	print()
	print("=== SIMULATION RESULTS ===")
	print("Number of runs: " + str(num_simulations))
	print("White wins: " + str(num_wins_white), "Black wins: " + str(num_wins_black))
	print()
	#The total number of game tree nodes expanded by each player in the course of the game.
	print("Average white nodes expanded per game: " + str(white_nodes / num_simulations))
	print("Average black nodes expanded per game: " + str(black_nodes / num_simulations))
	print()
	#The average number of nodes expanded per move and the average amount of time to make a move.
	print("Average nodes expanded per move: " + str(average_total_nodes / num_simulations))
	print("Average time per move: " + str(average_time_per_move / num_simulations))
	print()

	end_time = time.time()
	print("Time: " + str(end_time - start_time))
	print("Average time per game: " + str((end_time - start_time) / num_simulations))

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
	if is_white_turn_global:
		white_nodes += 1
	else:
		black_nodes += 1
	winner, utility, name = winner_exists(white_workers, black_workers)
	#check for winner first
	if winner:
		if (is_white_turn_global and name == "white") or (not is_white_turn_global and name == "black"):
			return utility
		else:
			return -utility
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
	if is_white_turn_global:
		white_nodes += 1
	else:
		black_nodes += 1
	winner, utility, name = winner_exists(white_workers, black_workers)
	#check for winner first
	if winner:
		if (is_white_turn_global and name == "white") or (not is_white_turn_global and name == "black"):
			return utility
		else:
			return -utility
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

def custom_heuristic_offensive(white_workers, black_workers, is_white_turn):
    whitetotal = 0
    blacktotal = 0
    totalweight = 0

    ##weights own positions more
    if is_white_turn:
        totalweight = np.sum(white_workers[:,1:]) - (7 * len(black_workers) - np.sum(black_workers[:, 1:]))
    else:
        totalweight = 7 * len(black_workers) - np.sum(black_workers[:,1:]) - np.sum(white_workers[:, 1:])
    
    ##find how many pieces you can capture
    ##[x,y]
    capturedPieces = 0
    if (is_white_turn): 
        for whiteworker in white_workers:
            for blackworker in black_workers:
                if ((blackworker[1] == whiteworker[1] + 1) and (blackworker[0] == whiteworker[0] + 1 or blackworker[0] == whiteworker[0] - 1)):
                    capturedPieces+=1
    else:
        for blackworker in black_workers:
            for whiteworker in white_workers:
                if ((whiteworker[1] == blackworker[1] - 1) and (whiteworker[0] == blackworker[0] + 1 or whiteworker[0] == blackworker[0] - 1)):
                    capturedPieces+=1
    
    return totalweight + random.random()

def custom_heuristic_defensive(white_workers, black_workers, is_white_turn):
    whitetotal = 0
    blacktotal = 0
    totalweight = 0
 
    ##weights the enemy positions more
    
    if is_white_turn:
        totalweight = 60 - (7 * len(black_workers) - np.sum(black_workers[:,1:]) - np.sum(white_workers[:, 1:]))
    else:
        totalweight = 60 - (np.sum(white_workers[:,1:]) - np.sum(black_workers[:, 1:]))
 
    ##find how many pieces you can block
    blockedPieces = 0
    if (is_white_turn):
        for whiteworker in white_workers:
            for blackworker in black_workers:
                if ((blackworker[1] == whiteworker[1] + 1) and (blackworker[0] == whiteworker[0])):
                    blockedPieces+=1
    else:
        for blackworker in black_workers:
            for whiteworker in white_workers:
                if ((whiteworker[1] == blackworker[1] - 1) and (whiteworker[0] == blackworker[0])):
                    blockedPieces+=1
 
    ##minimize opponent captures
    capturedPieces = 0
    if (is_white_turn):
        for whiteworker in white_workers:
            for blackworker in black_workers:
                if ((blackworker[1] == whiteworker[1] + 1) and (blackworker[0] == whiteworker[0] + 1 or blackworker[0] == whiteworker[0] - 1)):
                    capturedPieces+=1
    else:
        for blackworker in black_workers:
            for whiteworker in white_workers:
                if ((whiteworker[1] == blackworker[1] - 1) and (whiteworker[0] == blackworker[0] + 1 or whiteworker[0] == blackworker[0] - 1)):
                    capturedPieces+=1
    return 2*totalweight + (30-capturedPieces) + blockedPieces + random.random()
    
run_alphabeta()