from utils import * 
import sys
import heapq
import cProfile

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
NUM_ATTEMPTS = 0
def dumb_solution(file):
	"""
	The "dumb" solution to the flow free CSP 
	Uses random variable and value order and no forward checking (of any kind)
	The CSP is defined as follows:
		Variables: Each abstract pipe on the board 
		Values: The paths between the two pipe sources
		Constraints: The paths should never intersect or go off the bounds of the board

		A complete, consistent assignment will assign a path to each pipe without violating any constraints. 
		Assume that a complete, consistent assignment will leave no empty squares on the board. 
		Unsure if this assumption is warranted.

	Arguments: 
		file {string} - The name of the file that holds the board we want to solve

	Returns:
		Nothing. Writes the solution to an output file if it exists
	"""
	
	# Open the file and initialize the board and all pipes
	filepath = "Inputs/" + file
	board = parse_file(filepath)
	
	# Fill out the list of possible values 
	for pipe in board.pipes:
		start, end = pipe.get_sources()
		valid = board.get_empty()
		valid.append(end)
		visited = Path()
		pipe.set_paths(generate_paths(visited, start, end, valid))

	# Run a recursive BT search on all the pipes to find a complete, consistent assignment of paths (if it exists)
	assignment = []
	unassigned = board.get_pipes_copy()
	if dumb_BT(assignment, unassigned):
		assign_to_board(assignment, board)
		filepath = "output_dumb" + file[file.find("t") + 1:]
		write_to_file(filepath, board, NUM_ATTEMPTS)
	else:
		print("Cannot find a solution for this game")
	
def smart_solution(file):
	"""
	The "smart" solution to the flow free CSP 
	Selects the most constrained variable and then the least constraining value 
	Implements forward checking - every time a value is assigned to a variable, all intersecting paths are deleted. 
		If a Pipe ever has 0 valid paths left, we can immediately start backtracking
	The CSP is defined as follows:
		Variables: Each abstract pipe on the board 
		Values: The paths between the two pipe sources
		Constraints: The paths should never intersect or go off the bounds of the board

		A complete, consistent assignment will assign a path to each pipe without violating any constraints. 
		Assume that a complete, consistent assignment will leave no empty squares on the board. 
		Unsure if this assumption is warranted.

	Arguments: 
		file {string} - The name of the file that holds the board we want to solve

	Returns:
		Nothing. Writes the solution to an output file if it exists
	"""
	# Open the file and initialize the board and all pipes
	filepath = "Inputs/" + file
	board = parse_file(filepath)
	
	# Fill out the list of possible values 
	for pipe in board.pipes:
		start, end = pipe.get_sources()
		valid = board.get_empty()
		valid.append(end)
		visited = Path()
		pipe.set_paths(generate_paths(visited, start, end, valid))

	assignment = []
	unassigned = board.get_pipes_copy()
	heapq.heapify(unassigned)

	# Run a recursive BT search on all the pipes to find a complete, consistent assignment of paths (if it exists)
	if smart_BT(assignment, unassigned):
		assign_to_board(assignment, board)
		filepath = "output_smart" + file[file.find("t") + 1:]
		write_to_file(filepath, board, NUM_ATTEMPTS)
	else:
		print("Cannot find a solution for this game")
	
"""
# Forget about this for now
def composite_solution(file):
	#Attempts both the dumb and the smart assignment algorithms
	global NUM_ATTEMPTS
	filepath = "Inputs/" + file
	board_dumb = parse_file(filepath)
	
	# Fill out the list of possible values 
	for pipe in board_dumb.pipes:
		start, end = pipe.get_sources()
		valid = board_dumb.get_empty()
		valid.append(end)
		visited = Path()
		pipe.set_paths(generate_paths(visited, start, end, valid))

	board_smart = board_dumb.copy()

	assignment = []
	unassigned = board_dumb.get_pipes_copy()
	if dumb_BT(assignment, unassigned):
		assign_to_board(assignment, board_dumb)
		filepath = "output_composite" + file[file.find("t") + 1:]
		append_to_file(filepath, board_dumb, NUM_ATTEMPTS)
	else:
		print("Cannot find a solution for this game using dumb BT search")

	assignment = []
	unassigned = board_smart.get_pipes_copy()
	heapq.heapify(unassigned)

	NUM_ATTEMPTS = 0
	# Run a recursive BT search on all the pipes to find a complete, consistent assignment of paths (if it exists)
	if smart_BT(assignment, unassigned):
		assign_to_board(assignment, board_smart)
		filepath = "output_composite" + file[file.find("t") + 1:]
		append_to_file(filepath, board, NUM_ATTEMPTS)
	else:
		print("Cannot find a solution for this game using smart BT search")
"""

def generate_paths(visited, start, goal, valid):
	"""
	A DFS graph search algorithm that recursively generates all paths between two points on the board 
	Somewhat similar to a backtracking algorithm 
	Returns either when the algorithm has recursed to the end of the tree, or when the algorithm has found a path between the two sources 
	After it returns, it backtracks to the latest node where there were still valid routes to take
	
	Arguments:
		visited {Path} - A Path object that holds the coordinates that have so far been added to the path. Functions as a "visited" array
		start {tuple} - Represents the start coordinate. Updated recursively. 
		goal {tuple} - Represents the coordinate we are trying to get to 
		valid {list of tuples} - Holds the coordinates that we are allowed to search through. This is equal to board.get_empty() plus the goal state

	Returns:
		paths {list of Path objects} - Represents all paths between the two source coordinates in the pipe
	"""
	paths = []
	visited.add_coord(start)
	if start == goal: # Base case
		paths.append(visited)
		return paths
	for dir1 in DIRS: # Recursion and constraint checking
		nextCoord = (start[0] + dir1[0], start[1] + dir1[1])
		if nextCoord in valid:
			adjacent = 0
			for dir2 in DIRS:
				if (nextCoord[0] + dir2[0], nextCoord[1] + dir2[1]) in visited.get_path():
					adjacent += 1
			if adjacent > 1:
				continue
			paths.extend(generate_paths(visited.copy(), nextCoord, goal, valid))
	return paths

def dumb_BT(assignment, unassigned):
	"""
	A recursive backtracking algorithm to find a complete, consistent assignment for all pipes in a "dumb" way
	"Dumb" Implementation: random variable and value ordering, no forward checking
	Edits the assignment list in place

	Arguments:
		assignment {list of Pipe objects}: a list holding all pipes that currently have assignments
		unassigned {list of Pipe objects}: a list holding all pipes that currently do not have assignments

	Returns:
		True if a complete, consistent assignment has been found, False if it doesn't exist
	"""
	global NUM_ATTEMPTS
	if len(unassigned) == 0:
		if completion_check_full(assignment):
			return True
		else:
			return False
	pipe = random_selection(unassigned)
	unassigned.remove(pipe)
	while(len(pipe.get_paths()) != 0):
		path = random_selection(pipe.get_paths())
		pipe.remove_path(path)
		if consistency_check_partial(assignment, path):
			assignment.append(pipe)
			pipe.set_solution(path)
			NUM_ATTEMPTS += 1
			if dumb_BT(assignment, unassigned):
				return True
			else:
				assignment.remove(pipe)
	pipe.reset_paths()
	unassigned.append(pipe)
	return False
	
def smart_BT(assignment, unassigned):
	"""
	A recursive backtracking algorithm to find a complete, consistent assignment for all pipes in a "smart" way
	"Smart" Implementation: selects the most constrained variable and then the least constraining value
		Also implements forward checking by deleting intersecting paths everytime a value is assigned to a variable. 
		If a Pipe ever has 0 valid paths left, we can immediately start backtracking
	Edits the assignment list in place

	Arguments:
		assignment {list of Pipe objects}: a list holding all pipes that currently have assignments
		unassigned {priority queue of Pipe objects}: a list holding all pipes that currently do not have assignments

	Returns:
		True if a complete, consistent assignment has been found, False if it doesn't exist
	"""
	global NUM_ATTEMPTS
	if len(unassigned) == 0:
		if completion_check_full(assignment):
			return True
		else:
			return False
	pipe = heapq.heappop(unassigned)
	num_removed = 0
	while(len(pipe.get_paths()) != 0):
		path = lcv_selection(pipe.get_paths())
		pipe.remove_path(path)
		num_removed += 1
		if consistency_check_partial(assignment, path):
			assignment.append(pipe)
			pipe.set_solution(path)
			NUM_ATTEMPTS += 1
			num_pruned = {}
			forward_checking(path, unassigned, num_pruned)
			if check_empty(unassigned):
				revert_pruning(unassigned, num_pruned)
				continue
			if smart_BT(assignment, unassigned):
				return True
			else: # No valid assignments were found
				revert_pruning(unassigned, num_pruned)
				assignment.remove(pipe)
	for j in range(num_removed, 0, -1):
		pipe.remove_from_discarded_most_recent()
	heapq.heappush(unassigned, pipe)
	return False

def print_usage():
	print("To use:\npython part1.py  [dumb | smart] [input55 | input77 | input88 | input99].txt")

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print_usage()
	else:
		if sys.argv[1] == "dumb":
			for i in range(2, len(sys.argv)):
				file = sys.argv[i]
				dumb_solution(file)
		elif sys.argv[1] == "smart":
			for i in range(2, len(sys.argv)):
				file = sys.argv[i]
				smart_solution(file)
		"""
		elif sys.argv[1] == "composite":
			for i in range(2, len(sys.argv)):
				file = sys.argv[i]
				composite_solution(file)
		"""