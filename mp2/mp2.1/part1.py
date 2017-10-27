from utils import * # hm
import sys

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def dumb_solution(file):
	file = "inputs/" + file
	board = parse_file(file)
	for pipe in board.pipes:
		sources = pipe.get_sources()
	for pipe in board.pipes:
		start, end = pipe.get_sources()
		valid = board.get_empty()
		valid.append(end)
		frontier = []
		frontier.append(start)
		visited = Path()
		print(pipe.get_letter())
		#print("Current visited: {0}".format(visited))
		pipe.set_paths(generate_paths(frontier, visited, end, valid))
	for pipe in board.pipes:
		print(pipe)

def generate_paths(frontier, visited, goal, valid):
	"""
	A DFS graph search algorithm that recursively generates all paths between two points on the board 
	Somewhat similar to a backtracking algorithm 
	Returns either when the algorithm has recursed to the end of the tree, or when the algorithm has found a path between the two sources 
	After it returns, it backtracks to the latest node where there were still valid routes to take
	
	Arguments:
		frontier {list of tuples} - A stack that holds all possible nodes that we still want to try 
		visited {Path} - A Path object that holds the coordinates that have so far been added to the path. Functions as a "visited" array
		goal {tuple} - Represents the coordinate we are trying to get to 
		valid {list of tuples} - Holds the coordinates that we are allowed to search through. This is equal to board.get_empty() plus the goal state

	Returns:
		paths {list of Path objects} - Represents all paths between the two source coordinates in the pipe
	"""
	# The back tracking is not working.
	# Figure out why
	print(visited)
	paths = []
	if len(frontier) == 0: 
		if visited.back() == goal:
			paths.append(visited)
		return paths
	curr = frontier.pop()
	visited.add_coord(curr)
	if curr == goal:
		paths.append(visited)
		return paths
	for dir1 in DIRS:
		nextCoord = (curr[0] + dir1[0], curr[1] + dir1[1])
		if nextCoord in valid:
			adjacent = 0
			for dir2 in DIRS:
				if (nextCoord[0] + dir2[0], nextCoord[1] + dir2[1]) in visited.get_path():
					adjacent += 1
			if adjacent > 1:
				continue 
			frontier.append(nextCoord)
	paths.extend(generate_paths(frontier.copy(), visited, goal, valid))
	# print(paths)
	return paths

def smart_solution(file):
	file = "inputs/" + file
	board = parse_file(file)

def print_usage():
	print("To use:\npython part1.py  [dumb | smart] [input55 | input77 | input88 | input99 | input10101 | input10102].txt")

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print_usage()
	if sys.argv[1] == 'dumb':
		for i in range(2, len(sys.argv)):
			file = sys.argv[i]
			dumb_solution(file)
	else:
		for i in range(2, len(sys.argv)):
			file = sys.argv[i]
			smart_solution(file)