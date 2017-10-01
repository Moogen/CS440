import queue as queue
from utils import manhattan, get_closest_dot, visited_to_path, visited_to_path2
import copy
from collections import deque

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def dfs(states, start, goal):
	stack, num_expanded = [], 0;
	visited = {} #the key is a coordinate, the value is the previous coordinate, this helps in constructing the final path
	stack.append(start)
	visited[start] = start

	while stack:
		coord = stack.pop()
		num_expanded += 1
		if coord == goal:
			print("Found goal using DFS")
			return visited, num_expanded

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			if nextCoord in states and nextCoord not in visited:
				stack.append(nextCoord)
				visited[nextCoord] = coord			

def bfs(states, start, goal):
	q, num_expanded = queue.Queue(), 0
	visited = {} #the key is a coordinate, the value is the previous coordinate, this helps in constructing the final path
	q.put(start)
	visited[start] = start
	while q:
		coord = q.get()
		num_expanded += 1
		if coord == goal:
			print("Found goal using BFS")
			return visited, num_expanded

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			if nextCoord in states and nextCoord not in visited:
				q.put(nextCoord)
				visited[nextCoord] = coord

def greedy(states, start, goal):
	visited = {}
	nodes, num_expanded = [], 0
	start_node = (start, manhattan(start, goal))
	nodes.append(start_node)
	visited[start]  = start
	while nodes:
		min_node = min(nodes, key = lambda x:x[1])
		coord = min_node[0]
		nodes.remove(min_node)
		num_expanded += 1
		if coord == goal:
			print("Found goal using Greedy BFS")
			return visited, num_expanded

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			if nextCoord in states and nextCoord not in visited:
				nodes.append((nextCoord, manhattan(nextCoord, goal)))
				visited[nextCoord] = coord

def astar_single(states, start, goal):
	visited = {}
	nodes, num_expanded = [], 0
	start_node = (start, manhattan(start, goal), 0)
	nodes.append(start_node)
	visited[start] = start
	while nodes:
		min_node = min(nodes, key = lambda x:x[1])
		coord, h, cost = min_node
		nodes.remove(min_node)
		num_expanded += 1
		if coord == goal:
			print("Found goal using A* (single goal)")
			return visited, num_expanded

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			val = visited.get(nextCoord)
			if nextCoord in states:
				if val is None:
					nodes.append((nextCoord, cost + manhattan(nextCoord, goal), cost+1))
					visited[nextCoord] = coord
				else:
					new_h = cost + manhattan(nextCoord, goal)
					if new_h < h:
						nodes.append((nextCoord, cost + manhattan(nextCoord, goal), cost+1))
						visited[nextCoord] = coord

def bfs2(states, start, goal):
	q, num_expanded = queue.Queue(), 0
	visited = {} #the key is a coordinate, the value is the previous coordinate, this helps in constructing the final path
	q.put((start, ()))
	visited[start] = (start, ())
	while q:
		coord, dots_eaten = q.get()
		num_expanded += 1
		if coord in goal and coord not in dots_eaten:
			old_key = (coord, dots_eaten)
			prev_val = visited.get(old_key)
			dots_eaten = list(dots_eaten)
			dots_eaten.append(coord)
			dots_eaten = tuple(sorted(dots_eaten))
			new_key = (coord, dots_eaten)
			visited[new_key] = prev_val

		if len(dots_eaten) == len(goal):
			print("tiny bfs done")
			return visited, num_expanded, (coord, tuple(sorted(goal)))

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			if nextCoord in states:
				key = (nextCoord, dots_eaten)
				nextNode = visited.get(key)
				if nextNode is None:
					q.put(key)
					visited[key] = (coord, dots_eaten)

"""
TODO:
1. Trace path with numbers instead of dots
2. Come up with a more clever heuristic function than manhattan distance
3. Come up with a more clever dot selection strategy than "pick whichever dot is closest to the current node" 
"""
def astar_multiple(states, start, goals):
	"""
	Implements A* search on a maze with multiple goals 
	Currently using the naive strategy of "next dot = closest dot to current point"

	Arguments: 
		states {set of tuples} -- represents the "empty" states in the maze
		start {tuple} -- the starting point 
		goals {list of tuples} -- list of dots that need to be reached

	Returns:
		list of tuples, int -- returns the path between the dots and the number of nodes expanded
	"""
	goals = copy.deepcopy(goals)
	num_expanded = 0
	coord = start
	path = deque()
	reached = deque()
	path.appendleft(start)

	while goals: 
		nodes, path_to_dot = [], {}
		goal = get_closest_dot(goals, coord) # Current dot selection strategy
		goals.remove(goal)
		reached.append(goal)
		start_node = (coord, manhattan(coord, goal), 0)
		nodes.append(start_node)
		path_to_dot[coord] = coord
		while nodes:
			min_node = min(nodes, key = lambda x:x[1])
			coord, _, cost = min_node
			nodes.remove(min_node)
			num_expanded += 1
			if coord == goal:
				print("Found goal at {0}".format(goal))
				path.extend(visited_to_path_deque(path_to_dot, goal))
				break

			for direction in DIRS:
				nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
				if nextCoord in states and nextCoord not in path_to_dot:
					nodes.append((nextCoord, cost + manhattan(nextCoord, goal), cost + 1))
					path_to_dot[nextCoord] = coord
				
	return path, reached, num_expanded