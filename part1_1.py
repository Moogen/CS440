from utils import parse_file, visited_to_path, print_sol
from maze_search import dfs, bfs, greedy, astar

FILE_NAMES = ['mediumMaze', 'bigMaze', 'openMaze'];
SEARCHES = [dfs, bfs, greedy, astar]

def init():
	for file_name in FILE_NAMES:
		input_path = 'mp1.1/inputs/' + file_name + '.txt'

		maze, states, pacman, dots = parse_file(input_path)
		for search in SEARCHES:
			visited, num_nodes_expanded = search(states, pacman, dots[0])
			sol = visited_to_path(visited, dots[0])
			output_path = 'mp1.1/outputs/' + file_name + '_sol_' + search.__name__ + '.txt'
			print_sol(output_path, maze, sol, num_nodes_expanded)

init()