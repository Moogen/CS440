from utils import * 
import sys

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
		Nothing. Prints out the solution at the end and writes it to an output file
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

	print(board)
	# Write the solution to the file
	filepath = "output" + file[file.find("t"):]
	write_to_file(filepath, board)
	

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
	# The back tracking is not working.
	# Figure out why
	# print(visited)
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
	print("To use:\npython part1.py  [dumb | smart] [input55 | input77 | input88 | input99 | input10101 | input10102].txt")

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