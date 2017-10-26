class Path: 
	"""
	A class representing the path between two pipe sources 
	In the context of a CSP, each path is a value
	Basically just a wrapper for a list of tuples because I don't want to deal with the ugliness of "list of list of tuples"
	"""

	def __init__(self):
		"""
		Initialize a Path object
		"""
		self.path = []

	def append_coord(self, coord): 
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
		"""
		self.letter = letter
		self.sources = []
		self.paths = []

	def __str__(self):
		"""
		Defined for print statements
		"""
		s = "Sources for pipe {0}: ".format(self.letter)
		for sources in self.sources:
			s += "{0} ".format(sources)
		return s

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

class Board:
	"""
	Represents the board on which the game is played 
	There will only be one per game
	"""
	def __init__(self):
		"""
		Initializes the Board object
		
		Arguments:
			pipes {list of Pipe objects}
		pipes is a list that holds Pipe objects and represents the variables of the game 
		empty is a list that holds the remaining coordinates that have not yet been assigned to. Coordinates will be represented as tuples. 
		"""
		self.pipes = []
		self.empty = []

	def __str__(self):
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

def parse_file(file):
	"""
	Parses an input file and converts it into useable data 

	Arguments:
		file {string} -- file name

	Returns:
		Board -- Returns an initialized board object
	"""
	board = Board()
	letters = []
	with open(file) as f:
		lines = f.readlines()
	lines = [line.strip() for line in lines]
	for x in range(len(lines)):
		line = lines[x]
		for y in range(len(line)):
			char = line[y]
			if char == '_':
				board.add_empty((x,y))
			elif char not in letters:
				pipe = Pipe(char)
				pipe.add_sources((x,y))
				board.add_pipe(pipe)
				letters.append(char)
				print(letters)
			elif char in letters: 
				pipe = board.get_pipe(char)
				pipe.add_sources((x,y))
	return board

if __name__ == "__main__":
	board = parse_file("mp2.1/inputs/input10102.txt");
	print(board)