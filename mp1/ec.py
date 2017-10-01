from utils import manhattan, visited_to_path
from graphics import *
import copy

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
"""
TODO:
1. Trace path with numbers instead of dots
2. Come up with a more clever heuristic function than manhattan distance
3. Come up with a more clever dot selection strategy than "pick whichever dot is closest to the current node" 
"""
def astar_ec(states, start, goals):
	goals = copy.deepcopy(goals)
	visited, path = {}, []
	distances = get_distances(states, goals)
	nodes, num_expanded = [], 0
	start_node = (start, distances.get(start), 0)
	nodes.append(start_node)
	visited[start] = start
	order = []
	while nodes:
		min_node = min(nodes, key = lambda x:x[1])
		coord, h, cost = min_node
		nodes.remove(min_node)
		num_expanded += 1
		if coord in goals:
			#print(coord)
			order.append(coord)
			goals.remove(coord)
			distances = get_distances(states, goals)
			path.extend(visited_to_path(visited, coord))
			visited.clear()
			visited[coord] = coord
			nodes = []

		if len(goals) ==0:
			print("done")
			return num_expanded, path, order

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			if nextCoord in states and nextCoord not in visited:
				nodes.append((nextCoord, cost + distances.get(nextCoord), cost+1))
				visited[nextCoord] = coord
			"""
			val = visited.get(nextCoord)
			if nextCoord in states:
				if val is None:
					nodes.append((nextCoord, cost + distances.get(nextCoord), cost+1))
					visited[nextCoord] = coord
				else:
					new_h = cost + distances.get(nextCoord)
					if new_h < h:
						nodes.append((nextCoord, new_h, cost+1))
						visited[nextCoord] = coord
						"""

def astar_ec_anim(states, start, goals, maze):
	win = GraphWin()

	goals = copy.deepcopy(goals)
	visited, path = {}, []
	distances = get_distances(states, goals)
	nodes, num_expanded = [], 0
	start_node = (start, distances.get(start), 0)
	nodes.append(start_node)
	visited[start] = start
	order = []
	while nodes:
		min_node = min(nodes, key = lambda x:x[1])
		coord, h, cost = min_node
		nodes.remove(min_node)
		num_expanded += 1
		if coord in goals:
			#print(coord)
			order.append(coord)
			goals.remove(coord)
			distances = get_distances(states, goals)
			path.extend(visited_to_path(visited, coord))
			visited.clear()
			visited[coord] = coord
			nodes = []

		if len(goals) ==0:
			print("done")
			return num_expanded, path, order

		for direction in DIRS:
			nextCoord = (coord[0] + direction[0], coord[1] + direction[1])
			if nextCoord in states and nextCoord not in visited:
				nodes.append((nextCoord, cost + distances.get(nextCoord), cost+1))
				visited[nextCoord] = coord


def get_distances(states, goals):
	results = {}
	for state in states:
		if state in goals:
			results[state] = 0
			continue

		smallest = -1
		for goal in goals:
			dist = manhattan(state, goal)
			smallest = dist if (dist < smallest or smallest == -1) else smallest
			if smallest == 1:
				break
		results[state] = smallest

	return results