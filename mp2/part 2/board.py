import numpy as np

#0 = space, 1 = white, 2 = black

board_width = 8
board_height = 8


def setup():
	board = np.array(np.zeros((8, 8)))
	board[:2] = 2
	board[6:8] = 1

	white_workers = np.array(np.zeros((board_width * 2, 2)))
	black_workers = np.array(np.zeros((board_width * 2, 2)))
	for y in range(2):
		for x in range(board_width):
			i = board_width * y + x
			white_workers[i] = [x,y]
			black_workers[i] = [x, board_height - 1 - y]

	return white_workers, black_workers


def check_bounds(coord):
	"""Returns if a worker is out of bounds or not
	
	[description]
	
	Arguments:
		coord {array} -- [description]
	
	Returns:
		bool -- if the worker is out of bounds or not
	"""
	x, y = coord
	if x < 0 or x >= board_width or y < 0 or y >= board_height:
		return False
	return True

def get_moves(white_workers, black_workers, white_turn):
	moves = np.array(np.zeros((0, 2, 2)))
	if white_turn:
		player_workers = white_workers
		opp_workers = black_workers
		direction = 1
	else:
		player_workers = black_workers
		opp_workers = white_workers
		direction = -1

	for worker in player_workers:
		x, y = worker
		#Try to go diagonally left
		coord = [x - 1, y + direction]
		if check_bounds(coord) and not (coord == player_workers).all(1).any():
			moves = np.insert(moves, 0, [worker, coord], 0)

		#Try to go straight
		coord = [x, y + direction]
		if check_bounds(coord) and not (coord == player_workers).all(1).any() and not (coord == opp_workers).all(1).any(): #this checks if the coord is already taken by an opposing piece
			moves = np.insert(moves, 0, [worker, coord], 0)

		#Try to go diagonally right
		coord = [x + 1, y + direction]
		if check_bounds(coord) and not (coord == player_workers).all(1).any():
			moves = np.insert(moves, 0, [worker, coord], 0)

	return moves

def make_move(white_workers, black_workers, white_turn, move):
	'''make a move and update the list of white and black workers
	
	[description]
	
	Arguments:
		white_workers {2d array} -- array of coordinates
		black_workers {2d array} -- array of coordinates
		white_turn {bool} -- is it the white player's turn
		move {2d array} -- array of cordinates. first coord is start, second coord is end
	
	Returns:
		2d array, 2d array -- returns white workers first, then the black workers
	'''
	start, end = move
	if white_turn:
		player_workers = np.copy(white_workers)
		opp_workers = np.copy(black_workers)
	else:
		player_workers = np.copy(black_workers)
		opp_workers = np.copy(white_workers)

	#remove the start coord from the player workers
	for i in range(player_workers.shape[0]):
		worker = player_workers[i]
		if (worker == start).all():
			player_workers = np.delete(player_workers, i, axis = 0)
			break

	#add end coord to player workers
	player_workers = np.vstack((player_workers, end))

	#remove the end coord from the opposing workers
	for i in range(opp_workers.shape[0]):
		worker = opp_workers[i]
		if (worker == end).all():
			opp_workers = np.delete(opp_workers, i, axis = 0)
			break

	if white_turn:
		return player_workers, opp_workers
	else:
		return opp_workers, player_workers

def winner_exists(white_workers, black_workers):
	#check for a winning white worker - y should be board_size-1
	if (board_height - 1) in white_workers[:, 1:] or len(black_workers) == 0:
		return True, 9999, "white"

	#check for a winning black worker - y should be 0
	if 0 in black_workers[:, 1:] or len(white_workers) == 0:
		return True, 9999, "black"

	return False, 0, "none"

def print_board(white_workers, black_workers):
	board = [["-" for i in range(board_width)]for j in range(board_height)]
	for worker in white_workers:
		board[int(worker[1])][int(worker[0])] = "W"
	for worker in black_workers:
		board[int(worker[1])][int(worker[0])] = "B"
	for i in range(board_height - 1, -1, -1):
		for j in board[i]:
			print(j, end = '')
		print("\n")

def winner_exists_ec(white_workers, black_workers):
	#check to see if white or black have less than 3 pieces
	if (len(white_workers) < 3):
		return True, 9999, "black"
	if (len(black_workers) < 3):
		return True, 9999, "white"
	#check if 3 workers
	whitecount = 0
	for worker in white_workers[:, 1:]:
		if (worker == board_height - 1):
			whitecount += 1
	if whitecount >= 3:
		return True, 9999, "white"
	blackcount = 0
	for worker in black_workers[:, 1:]:
		if (worker == 0):
			blackcount += 1
	if blackcount >= 3:
		return True, 9999, "black"
		
	return False, 0, "none"