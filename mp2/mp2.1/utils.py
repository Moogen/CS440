import math
import random 
import heapq

class Path: 
	"""
	A class representing the path between two pipe sources 
	In the context of a CSP, each path is a value
	Basically just a wrapper for a list of tuples because I don't want to deal with the ugliness of "list of list of tuples"
	"""
	def __init__(self):
		"""
		Initialize a Path object with a blank path
		"""
		self.path = []

	def __str__(self):
		"""
		Defined for print statements
		"""
		return "{0}".format(self.path)

	"""
	Overloading a bunch of operators for priority queue comparisons
	Not sure if all of these will be necessary, but I'm going to just throw them in just in case
	Plus they're simple so whatever
	"""
	def __lt__(self, other):
		"""
		Overloads the < operator for pipes
		other is assumed to be of type Path
		Returns true if the current path is shorter than the other path
		"""
		if len(self.path) < len(other.get_path()):
			return True
		else:
			return False

	def __le__(self, other):
		"""
		Overloads the <= operator for pipes
		other is assumed to be of type Path
		Returns true if the current path is shorter or equal in length with the other path
		"""
		if len(self.path) <= len(other.get_path()):
			return True
		else:
			return False

	def __gt__(self, other):
		"""
		Overloads the > operator for pipes
		other is assumed to be of type Path
		Returns true if the current path is longer than the other path
		"""
		if len(self.path) > len(other.get_path()):
			return True
		else:
			return False

	def __ge__(self, other):
		"""
		Overloads the >= operator for pipes
		other is assumed to be of type Path
		Returns true if the current path is longer or equal in length with the other path
		"""
		if len(self.path) >= len(other.get_path()):
			return True
		else:
			return False
		
	def __ne__(self, other):
		"""
		Overloads the != operator for pipes
		other is assumed to be of type Path
		Returns true if the current path is not equal in length with the other path
		"""
		if len(self.path) != len(other.get_path()):
			return True
		else:
			return False

	def add_coord(self, coord): 
		"""
		Append a coordinate to the end of the path. 
		*** There probably will not be situations where we need to insert coordinates into the middle/front
			Can write wrappers for those if necessary......... ***

		Arguments: 
			coord {tuple}: A coordinate to add to the path 
		"""
		self.path.append(coord)

	def remove_coord(self, coord):
		"""
		Removes a coordinate from the path (if it exists)

		Arguments:
			coord {tuple}: The coordinate
		"""
		self.path.remove(coord)

	def length(self):
		"""
		Returns the length of the path
		"""
		return len(self.path)

	def back(self):
		"""
		Returns the last coordinate in the path
		"""
		return self.path[len(self.path) - 1]

	def get_path(self):
		"""
		Returns the path
		"""
		return self.path

	def set_path(self, path):
		"""
		Set the path
		"""
		self.path = path

	def copy(self):
		"""
		Returns a copy of the Path object
		"""
		copy = Path()
		copy.set_path(self.path.copy())
		return copy
	

class Pipe:
	"""
	A class representing the pipes on the board 
	In the context of a CSP, each Pipe object is a variable
	"""
	def __init__(self, letter):
		"""
		Initialize a Pipe object 

		Arguments:
			letter {string}: A unique identifier for the pipe. Corresponds to the letter that represents the pipe on the board 
			sources {list of two tuples}: Represents the two coordinates for the pipe's sources. There will always be two tuples 
			paths {list of Path objects}: Holds all possible paths between the two coordinates. In the context of a CSP, paths is the set of values that can be 
				assigned to the each variable/pipe
			solution {Path object}: Holds the solution path
		"""
		self.letter = letter
		self.sources = []
		self.paths = []
		self.discarded = []
		self.solution = Path()

	def __str__(self):
		"""
		Defined for print statements
		"""
		s = "Sources for pipe {0}: ".format(self.letter)
		for sources in self.sources:
			s += "{0} ".format(sources)
		s += "\n\tPaths: "
		for path in self.paths:
			s += "{0} ".format(path)
		s += "\n"
		if self.solution != Path():
			s += "\tSolution: {0}".format(self.solution)
		return s

	"""
	Overloading a bunch of operators for priority queue comparisons
	Not sure if all of these will be necessary, but I'm going to just throw them in just in case
	Plus they're simple so whatever
	"""
	def __lt__(self, other):
		"""
		Overloads the < operator for pipes
		other is assumed to be of type Pipe
		Returns true if the size of the current pipe's paths list is less than the size of other's paths list
		"""
		if len(self.paths) < len(other.get_paths()):
			return True
		else:
			return False

	def __le__(self, other):
		"""
		Overloads the <= operator for pipes
		other is assumed to be of type Pipe
		Returns true if the size of the current pipe's paths list is less than or equal to the size of other's paths list
		"""
		if len(self.paths) <= len(other.get_paths()):
			return True
		else:
			return False

	def __gt__(self, other):
		"""
		Overloads the > operator for pipes
		other is assumed to be of type Pipe
		Returns true if the size of the current pipe's paths list is greater than the size of other's paths list
		"""
		if len(self.paths) > len(other.get_paths()):
			return True
		else:
			return False

	def __ge__(self, other):
		"""
		Overloads the >= operator for pipes
		other is assumed to be of type Pipe
		Returns true if the size of the current pipe's paths list is greater than or equal to the size of other's paths list
		"""
		if len(self.paths) >= len(other.get_paths()):
			return True
		else:
			return False
		
	def __ne__(self, other):
		"""
		Overloads the != operator for pipes
		other is assumed to be of type Pipe
		Returns true if the size of the current pipe's paths list is not equal to the size of other's paths list
		"""
		if len(self.paths) != len(other.get_paths()):
			return True
		else:
			return False
	
	def get_letter(self):
		"""
		Returns the pipe's letter
		"""
		return self.letter

	def add_sources(self, source):
		"""
		Adds the sources of the pipe
		Should be called exactly twice when initializing the pipe

		Arguments:
			source {tuple}: A source
		"""
		self.sources.append(source)

	def set_sources(self, sources):
		"""
		Setter method for sources
		"""
		self.sources = sources

	def get_sources(self):
		"""
		Getter method for sources
		"""
		return self.sources

	def set_paths(self, paths):
		"""
		Setter method for paths
		Applies heapsort to paths to make sure it is a min-heap
		"""
		self.paths = paths
		heapq.heapify(self.paths)
	
	def remove_path(self, path):
		"""
		Removes a path from paths and puts it into the discarded list
		Maintains paths as a min-heap. Discarded is NOT a heap
		"""
		for i in range(len(self.paths)):
			if path == self.paths[i]:
				self.discarded.append(self.paths.pop(i))
				break
		heapq.heapify(self.paths)

	def get_paths(self):
		"""
		Getter method for paths
		"""
		return self.paths

	def set_solution(self, path):
		"""
		Setter method for solution
		"""
		self.solution = path

	def get_solution(self):
		"""
		Getter method for solution
		"""
		return self.solution

	def set_discarded(self, discarded):
		"""
		Setter method for discarded
		"""
		self.discarded = discarded

	def get_discarded(self):
		"""
		Getter method for discarded
		"""
		return self.discarded

	def remove_from_discarded(self, path):
		"""
		Removes a path from the discarded list and puts it back into paths
		Maintains paths as a min-heap
		"""
		if path in self.discarded:
			heapq.heappush(self.paths, self.discarded.remove(path))

	def remove_from_discarded_most_recent(self):
		"""
		Removes the most recently added path and moves it back to paths
		Maintains paths as a min-heap
		"""
		heapq.heappush(self.paths, self.discarded.pop())

	def reset_paths(self):
		"""
		Resets the paths list by adding all paths in discarded back into paths
		Makes sure to maintain the heap properties of paths
		"""
		if len(self.paths) == 0:
			self.paths = self.discarded
			self.discarded = []
			heapq.heapify(self.paths)
		else:
			for path in self.discarded:
				self.remove_from_discarded(path)

	def get_lcv(self):
		"""
		If paths is not empty, returns the shortest path
		"""
		lcv = heapq.heappop(self.paths)
		self.discarded.append(lcv)
		return lcv

	def copy(self):
		"""
		Returns a copy of this pipe
		"""
		copy = Pipe(self.get_letter())
		copy.set_sources(self.get_sources().copy())
		copy.set_paths(self.get_paths().copy())
		copy.set_solution(self.get_solution().copy())
		copy.set_discarded(self.get_discarded().copy())
		return copy

class Board:
	"""
	Represents the board on which the game is played 
	There will only be one per game
	"""
	def __init__(self):
		"""
		Initializes the Board object
		pipes is a list that holds Pipe objects and represents the variables of the game 
		empty is a list that holds the remaining coordinates that have not yet been assigned to. Coordinates will be represented as tuples. 
		
		Arguments:
			pipes {list of Pipe objects}
		"""
		self.pipes = []
		self.empty = []
		self.dimension = 0

	def __str__(self):
		"""
		Defined for print statements
		"""
		s = "Pipes: \n"
		for pipe in self.pipes:
			s += "{0}".format(pipe)
			s += "\n"
		s += "Unassigned coordinates: \n"
		for coord in self.empty:
			s += "{0} ".format(coord)
		return s

	def add_pipe(self, pipe):
		"""
		Adds a Pipe object to pipes
		"""
		self.pipes.append(pipe)

	def get_pipe(self, letter):
		"""
		Arguments:
			letter {string}: The requested letter 

		Returns: 
			Pipe - the pipe corresponding to the requested letter
		"""
		for pipe in self.pipes:
			if pipe.get_letter() == letter:
				return pipe
		# Assume that we never request an invalid letter. Probably want to add error checking 

	def set_pipes(self, pipes):
		"""
		Setter method for pipes
		"""
		self.pipes = pipes

	def get_pipes(self):
		"""
		Getter method for pipes
		"""
		return self.pipes

	def get_pipes_copy(self):
		"""
		Gets a copy of the pipes list
		"""
		copy = []
		for pipe in self.get_pipes():
			copy.append(pipe.copy())
		return copy

	def remove_pipe(self, pipe):
		"""
		Removes a Pipe object
		"""
		self.pipes.remove(pipe)

	def get_num_pipes(self):
		"""
		Returns the number of pipes in the board
		"""
		return len(self.pipes)

	def add_empty(self, coord):
		"""
		Adds a coordinate to empty
		"""
		self.empty.append(coord)

	def remove_empty(self, coord):
		"""
		Removes a coordinate from empty, if it exists
		"""
		if coord in self.empty:
			self.empty.remove(coord)

	def set_empty(self, empty):
		"""
		Setter function for empty
		"""
		self.empty = empty
		
	def get_empty(self):
		"""
		Getter function for empty
		"""
		return self.empty.copy()

	def set_dimension(self, dimension):
		"""
		Setter function for dimension
		"""
		self.dimension = dimension

	def get_dimension(self):
		"""
		Getter function for dimension
		"""
		return self.dimension

	def copy(self):
		"""
		Returns a copy of this Board object
		"""
		copy = Board()
		copy.set_pipes(self.get_pipes_copy())
		copy.set_empty(self.get_empty().copy())
		copy.set_dimension(self.get_dimension())

def parse_file(file):
	"""
	Parses an input file and converts it into useable data 

	Arguments:
		file {string}: file name

	Returns:
		Board: Returns an initialized board object
	"""
	board = Board()
	letters = []
	with open(file) as f:
		lines = f.readlines()
	lines = [line.strip() for line in lines]
	board.set_dimension(len(lines))
	for y in range(len(lines)):
		line = lines[y]
		for x in range(len(line)):
			char = line[x]
			if char == '_':
				board.add_empty((x,y))
			elif char not in letters:
				pipe = Pipe(char)
				pipe.add_sources((x,y))
				board.add_pipe(pipe)
				letters.append(char)
			elif char in letters: 
				pipe = board.get_pipe(char)
				pipe.add_sources((x,y))
	return board

def write_to_file(file, board, num_attempts):
	"""
	A function that writes a board state to a text file

	Arguments:
		file {string}: The name of the output file
		board {Board object}: The current state of the board

	Returns:
		Nothing, but writes to a file
	"""
	state = []
	for i in range(board.get_dimension()):
		state.append(["_"] * board.get_dimension())
	for pipe in board.get_pipes():
		path = pipe.get_solution()
		letter = pipe.get_letter()
		for coord in path.get_path(): 
			state[coord[0]][coord[1]] = letter
	file = "Outputs/Test/" + file
	with open(file, mode="w") as f:
		for y in range(len(state)):
			for x in range(len(state[0])):
				f.write("{0}".format(state[x][y]))
			f.write("\n")
		f.write("Number of attempted assignments: {0}".format(num_attempts))

def append_to_file(file, board, num_attempts):
	"""
	A function that writes a board state to a text file

	Arguments:
		file {string}: The name of the output file
		board {Board object}: The current state of the board

	Returns:
		Nothing, but writes to a file
	"""
	state = []
	for i in range(board.get_dimension()):
		state.append(["_"] * board.get_dimension())
	for pipe in board.get_pipes():
		path = pipe.get_solution()
		letter = pipe.get_letter()
		for coord in path.get_path(): 
			state[coord[0]][coord[1]] = letter
	file = "Outputs/" + file
	with open(file, mode="w+") as f:
		for y in range(len(state)):
			for x in range(len(state[0])):
				f.write("{0}".format(state[x][y]))
			f.write("\n")
		f.write("Number of attempted assignments: {0}".format(num_attempts))

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

def lcv_selection(paths):
	"""
	Selects the least constraining path 
	For now, assumes that the path with the shortest length will be the least constraining 
	Prooooooobably want to change that later
	"""
	smallest_path = paths[0]
	for i in range(1, len(paths)):
		other_path = paths[i]
		if len(other_path.get_path()) < len(smallest_path.get_path()):
			smallest_path = other_path
	return smallest_path

def check_intersection(path1, path2):
	"""
	A function that checks if two paths intersect 
	Runs in O(n^2) time

	Arguments:
		path1, path2 {Path objects}: we want to confirm or deny the intersection of these two paths

	Returns:
		True if the two paths intersect. False if they don't
	"""
	p1 = path1.get_path()
	p2 = path2.get_path()
	for coord1 in p1:
		for coord2 in p2:
			if coord1 == coord2: 
				return True
	return False

def forward_checking(path, unassigned, removed):
	"""
	Enacts forward checking on the remaining pipes 
	Basically moves all paths in the unassigned pipes that intersect the given path into the "discarded" stack
	Keeps track of how many paths were discarded for each pipe
	Since discarded is a stack, the n most recently added paths correspond to the value n associated with each pipe in the removed dictionary
	Damn I'm clever ;^)

	Arguments:
		path {Path object}: the path we are currently assigning to a Pipe
		unassigned {list of Pipe objects}: the remaining pipes in the puzzle that don't have an assignment yet
		removed {dictionary of strings to ints -- {Pipe.get_letter() : # paths removed by forward checking}}: keeps track of the number of removed paths for recursive purposes
	"""
	if len(unassigned) == 0:
		return None
	for pipe in unassigned:
		for path2 in pipe.get_paths():
			if check_intersection(path, path2):
				pipe.remove_path(path2)
				if pipe.get_letter() in removed.keys():
					removed[pipe.get_letter()] += 1
				else:
					removed[pipe.get_letter()] = 1

def revert_pruning(pipes, removed):
	"""
	Puts the paths back where they belonged before they were pruned

	Arguments:
		pipes {list of Pipe objects}: The pipes that need to be reverted. Represents the unassigned pipes in BT
		removed {dictionary of Pipe identifiers (i.e., letters of type string) to ints (i.e., the number of paths that were pruned)}

	Returns:
		Nothing
	"""
	for letter in removed.keys():
		for pipe in pipes:
			if pipe.get_letter() == letter:
				for j in range(removed[letter], 0, -1):
					pipe.remove_from_discarded_most_recent()

def check_empty(pipes):
	"""
	A helper function that checks if any of the pipes given have no available paths 

	Arguments: 
		pipes {list of Pipe objects}: The pipes under consideration 

	Returns:
		True if one of the pipes is empty, False otherwise
	"""
	for pipe in pipes:
		if len(pipe.get_paths()) == 0:
			return True
	return False

def assign_to_board(assignment, board):
	"""
	Helper function that copies the complete, consistent assignment to the board object
	"""
	for pipe in assignment:
		board.get_pipe(pipe.get_letter()).set_solution(pipe.get_solution())

if __name__ == "__main__":
	board = parse_file("Inputs/input55.txt");
	print(board)