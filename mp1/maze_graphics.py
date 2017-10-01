from graphics import *

CELL_SIZE = 20
PACMAN, WALL, DOT = 'P', '%', '.'

def draw_maze(maze):
	width = len(maze[0])
	height = len(maze)
	win = GraphWin('BigMaze', width * CELL_SIZE, height * CELL_SIZE)
	print(width, height)

	for x in range(width):
		for y in range(height):
			c = maze[y][x]
			coord = (x, y)

			if c == WALL:
				draw_wall(win, coord)
			elif c == PACMAN:
				draw_pacman(win, coord)
			else:
				draw_empty(win, coord)
			if c == DOT:
				draw_dot(win, coord)
	return win

def draw_rect(win, coord, color):
	x, y = coord
	x *= CELL_SIZE
	y *= CELL_SIZE
	cell = Rectangle(Point(x, y), Point(x + CELL_SIZE, y + CELL_SIZE))
	cell.setFill(color)
	cell.setOutline(color)
	cell.draw(win)

def draw_wall(win, coord):
	draw_rect(win, coord, 'gray')

def draw_empty(win, coord):
	draw_rect(win, coord, 'white')

def draw_pacman(win, coord):
	draw_rect(win, coord, 'blue')

def draw_path(win, coord):
	draw_rect(win, coord, 'cyan')

def draw_extends(win, coord):
	draw_rect(win, coord, 'yellow')

def draw_dot(win, coord):
	x, y = coord
	x *= CELL_SIZE
	y *= CELL_SIZE
	cell = Circle(Point(x + CELL_SIZE/2, y + CELL_SIZE/2), CELL_SIZE / 4)
	cell.setFill('red')
	cell.setOutline('red')
	cell.draw(win)

def draw_sol(win, path, order):
	l = len(path)
	j = 0
	for i in range(l):
		coord = reversed(path[i])
		draw_path(win, coord)

	for i in range(len(order)):
		y,x = order[i]
		label = Text(Point(x * CELL_SIZE + CELL_SIZE/2, y * CELL_SIZE + CELL_SIZE/2), i)
		label.setSize(8)
		label.draw(win)
	win.getMouse()
	win.close()