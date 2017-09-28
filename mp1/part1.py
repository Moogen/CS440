from utils import parse_file, visited_to_path, print_sol
from maze_search import dfs, bfs, greedy, astar_single, astar_multiple
import sys

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
		sol, num_nodes_expanded = astar_multiple(states, pacman, dots)
		output_path = 'mp1.2/outputs/' + file_name + '_sol_astar_multiple.txt'
		print_sol(output_path, maze, sol, num_nodes_expanded)

def part1_ec():
	input_path = 'mp1_ec/inputs/bigDots.txt'
	output_path = 'mp1_ec/outputs/bigDots_sol.txt'

	maze, states, pacman, dots = parse_file(input_path)
	sol, num_nodes_expanded = astar_multiple(states, pacman, dots)
	print_sol(output_path, maze, sol, num_nodes_expanded)
	
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
		else:
			print("Option {0} is invalid".format(i))
			print_usage()