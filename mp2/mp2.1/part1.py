from utils import * 
import sys
import random 
import math

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

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
		filepath = "output" + file[file.find("t") + 1:]
		write_to_file(filepath, board)
	else:
		print("Cannot find a solution for this game")
	
def assign_to_board(assignment, board):
	"""
	Helper function that copies the complete, consistent assignment to the board object
	"""
	for pipe in assignment:
		board.get_pipe(pipe.get_letter()).set_solution(pipe.get_solution())

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
	if len(unassigned) == 0:
		if completion_check_full(assignment):
			return True
		else:
			return False
	tested_paths = []
	pipe = random_selection(unassigned)
	unassigned.remove(pipe)
	while(len(pipe.get_paths()) != 0):
		path = random_selection(pipe.get_paths())
		pipe.remove_path(path)
		tested_paths.append(path)
		if consistency_check_partial(assignment, path):
			assignment.append(pipe)
			pipe.set_solution(path)
			if dumb_BT(assignment, unassigned):
				return True
			else:
				assignment.remove(pipe)
	pipe.set_paths(tested_paths)
	unassigned.append(pipe)
	return False

def completion_check_full(assignment):
	"""
	Checks if the board has a complete, consistent assignment

	Arguments:
		assignment {list of Pipe objects}: represents all pipes that have assignments

	Returns:
		True if the board's current assignment is complete and consistent, False if it isn't
	"""
	if len(assignment) == 0:
		return False
	for pipe in assignment:
		if pipe.get_solution().length() == 0:
			return False
	for i in range(len(assignment) - 1):
		path = assignment[i].get_solution()
		for j in range(i + 1, len(assignment)):
			other_path = assignment[j].get_solution()
			if check_intersection(path, other_path): # The paths intersect!
				return False
	return True

def consistency_check_partial(assignment, path):
	"""
	Checks if a path is consistent with the current assignment
	
	Arguments:
		assignment {list of Pipe objects}: represents all pipes that have assignments
		path {Path object}: the path we want to check 

	Returns:
		True if the path is consistent with the assignment, False if it isn't
	"""
	if len(assignment) == 0:
		return True
	for pipe in assignment:
		if check_intersection(path, pipe.get_solution()):
			return False
	return True

def random_selection(obj_list):
	"""
	Randomly select something out of the list of objects and return it
	obj_list will either be a list of pipes (i.e., get a random pipe) or a list of paths (i.e., get a random path)
	"""
	bound = len(obj_list)
	return obj_list[math.floor(bound * random.random())]

def smart_solution(file):
	# Open the file and initialize the board and all pipes
	file = "Inputs/" + file
	board = parse_file(file)
	
	# Fill out the list of possible values 
	for pipe in board.pipes:
		start, end = pipe.get_sources()
		valid = board.get_empty()
		valid.append(end)
		visited = Path()
		pipe.set_paths(generate_paths(visited, start, end, valid))
	
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