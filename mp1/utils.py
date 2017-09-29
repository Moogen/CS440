import copy
import math
from collections import deque

PACMAN, WALL, DOT = 'P', '%', '.'

def parse_file(file):
	"""Parses a maze text file into useable data
	
	Arguments:
		file {string} -- file name
	
	Returns:
		list, set, tuple, list of tuple -- Returns the maze in list format, a set of possible states, the starting location (pacman), and a list of dot locations.
	"""
	maze = []
	states = set()
	pacman = (0,0)
	dots = []

	with open(file) as f:
		lines = f.readlines()
	lines = [line.strip() for line in lines]
	for x in range(len(lines)):
		line = lines[x]
		maze.append([])
		for y in range(len(line)):
			c = line[y]
			maze[x].append(c)
			if c == DOT:
				dots.append((x, y))
			if c == PACMAN:
				pacman = (x,y)
			if c != WALL:
				states.add((x,y))
	return maze, states, pacman, dots

def manhattan(p1, p2):
	"""Returns the manhattan distance between two points.
	
	Arguments:
		p1 {tuple} -- first point
		p2 {tuple} -- second point
	
	Returns:
		int -- manhattan distance
	"""
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def print_sol(output_path, maze, sol, num_nodes_expanded):
	"""Write documentation for this

	Arguments:
		output_path {string} -- file name
		maze {list} -- a list carrying the maze
		sol {list} -- a list of tuples carrying the solution 
		num_nodes_expanded {int} -- the number of nodes expanded (lol)
	"""
	maze = copy.deepcopy(maze)
	for c in sol:
		maze[c[0]][c[1]] = '.'

	with open(output_path, mode='w') as f:
		for x in range(len(maze)):
			for y in range(len(maze[0])):
				f.write(maze[x][y])
			f.write('\n')
		f.write('Path cost: ' + str(len(sol)) + '\n')
		f.write('Nodes expanded: ' + str(num_nodes_expanded))

def print_sol_multiple(output_path, maze, sol, order, num_nodes_expanded):
	maze = copy.deepcopy(maze)
	num = 0
	for dot in order:
		if num < 10:
			maze[dot[0]][dot[1]] = num
			num += 1
			if num == 10:
				num = 97
		else:
			maze[dot[0]][dot[1]] = chr(num)
			num += 1
			if num == 123:
				num = 65 # We are assuming there will not be more than 62 dots

	with open(output_path, mode='w') as f:
		for x in range(len(maze)):
			for y in range(len(maze[0])):
				f.write(str(maze[x][y]))
			f.write('\n')
		f.write('Solution cost: ' + str(len(sol) - 1) + '\n') # len(sol) - 1 because sol includes the start node
		f.write('Nodes expanded: ' + str(num_nodes_expanded))

def visited_to_path(visited, goal):
	path = []
	curr, prev = goal, visited[goal]
	while curr != prev:
		path.append(curr)
		curr = prev
		prev = visited[prev]
	return path

def visited_to_path_deque(visited, goal):
	path = deque()
	curr, prev = goal, visited[goal]
	while curr != prev:
		path.appendleft(curr)
		curr = prev
		prev = visited[prev]
	return path

def get_closest_dot(dots, curr) :
	"""Returns the dot closest to the current coordinates

	Arguments: 
		dots {list of tuples} -- coordinates for all the dots that we still have to collect
		curr {tuple} -- coordinates of our current location

	Returns: 
		tuple -- the dot we want to go to next 
	"""
	dist = math.inf
	next_dot = (0, 0)
	for dot in dots:
		heur = manhattan(dot, curr)
		if heur < dist: 
			dist = heur
			next_dot = dot
	return next_dot