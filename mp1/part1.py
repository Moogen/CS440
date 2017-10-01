from utils import parse_file, visited_to_path, visited_to_path2, print_sol, print_sol_multiple
from maze_search import dfs, bfs, bfs2, greedy, astar_single, astar_multiple
from ec import get_distances, astar_ec, astar_p2
import sys
from collections import deque

FILE_NAMES_1 = ['mediumMaze', 'bigMaze', 'openMaze'];
FILE_NAMES_2 = ['tinySearch', 'smallSearch', 'mediumSearch']
SEARCHES_1 = [dfs, bfs, greedy, astar_single]

def part1_1():
	for file_name in FILE_NAMES_1:
		input_path = 'mp1.1/inputs/' + file_name + '.txt'
		print("Now searching: {0}.txt".format(file_name))
		maze, states, pacman, dots = parse_file(input_path)
		for search in SEARCHES_1:
			visited, num_nodes_expanded = search(states, pacman, dots[0])
			sol = visited_to_path(visited, dots[0])
			output_path = 'mp1.1/outputs/' + file_name + '_sol_' + search.__name__ + '.txt'
			print_sol(output_path, maze, sol, num_nodes_expanded)

def part1_2():
	for file_name in FILE_NAMES_2:
		input_path = 'mp1.2/inputs/' + file_name + '.txt'
		maze, states, pacman, dots = parse_file(input_path)
		print("Now searching: {0}.txt".format(file_name))
		num_nodes_expanded, sol, order = astar_ec(states, pacman, dots)
		output_path = 'mp1.2/outputs/' + file_name + '_sol_astar_multiple.txt'
		print_sol_multiple(output_path, maze, sol, order, num_nodes_expanded)

def test():
	input_path = 'mp1_ec/inputs/' + 'bigDots' + '.txt'
	maze, states, pacman, dots = parse_file(input_path)
	print("Now searching: {0}.txt".format('bigDots'))
	results = get_distances(states, dots)
	for a in results:
		print(a, results[a])
	#visited, num_nodes_expanded, end = bfs2(states, pacman, dots)
	#sol = visited_to_path2(visited, end)
	#output_path = 'mp1.2/outputs/' + 'bigDots' + '_sol_astar_multiple.txt'
	#print_sol(output_path, maze, sol, num_nodes_expanded)

def part1_ec():
	input_path = 'mp1_ec/inputs/bigDots.txt'
	output_path = 'mp1_ec/outputs/bigDots_sol.txt'

	maze, states, pacman, dots = parse_file(input_path)
	num_expanded, visited = astar_ec(states, pacman, dots)
	print(num_expanded, len(visited))
	
def print_usage():
	print("To use:\npython part1.py [part1_1 | part1_2 | part1_ec]")

if __name__ == "__main__":
	if(len(sys.argv) == 1): 
		print_usage()

	for i in range(1, len(sys.argv)):
		func = sys.argv[i]
		if func == "part1_1": 
			part1_1()
		elif func == "part1_2": 
			part1_2()
		elif func == "part1_ec":
			part1_ec()
		elif func == "test":
			test()
		else:
			print("Option {0} is invalid".format(i))
			print_usage()