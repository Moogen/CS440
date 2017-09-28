import queue as queue
from utils import manhattan

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def dfs(states, start, goal):
	stack, num_expanded = [], 0;
	visited = {} #the key is a coordinate, the value is the previous coordinate, this helps in constructing the final path
	stack.append(start)
	visited[start] = start

	while stack:
		coord = stack.pop()
		if coord == goal:
			return visited, num_expanded

		num_expanded += 1
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
			print("found goal")
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
			print("found goal")
			return visited, num_expanded

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			if nextCoord in states and nextCoord not in visited:
				nodes.append((nextCoord, manhattan(nextCoord, goal)))
				visited[nextCoord] = coord

def astar(states, start, goal):
	visited = {}
	nodes, num_expanded = [], 0
	start_node = (start, manhattan(start, goal), 0)
	nodes.append(start_node)
	visited[start]  = start
	while nodes:
		min_node = min(nodes, key = lambda x:x[1])
		coord, _, cost = min_node
		nodes.remove(min_node)
		num_expanded += 1
		if coord == goal:
			print("found goal")
			return visited, num_expanded

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			if nextCoord in states and nextCoord not in visited:
				nodes.append((nextCoord, cost + manhattan(nextCoord, goal), cost+1))
				visited[nextCoord] = coord