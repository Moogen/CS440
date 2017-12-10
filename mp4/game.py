import numpy as np

class Game:

	def __init__(self):
		self.paddle_height = 0.2
		self.ball_x = 1
		self.ball_y = 1
		self.velocity_x = 0.03
		self.velocity_y = 0.01
		self.paddle_y = 0.5 - self.paddle_height

		#q learning stuff
		self.state_size = 10369
		self.Q = np.zeros([self.state_size, 3])

	def convert_to_discrete(self):
		self.discrete_velocity_x = np.sign(self.velocity_x)
		self.discrete_velocity_y = np.sign(self.velocity_y)
		if np.abs(self.velocity_y) < 0.015:
			self.discrete_velocity_y = 0
		self.discrete_paddle_y = np.floor(12 * self.paddle_y / (1 - self.paddle_height))
		if self.paddle_y == 1 - self.paddle_height:
			self.discrete_paddle_y = 11

	def get_cell(self):
		"""
		Get a cell representation of the ball position on a 12 x 12 grid
		
		Returns (0-11, 0-11) as the coordinates and an index representation (1, 0) = 1, (1, 1) = 13, etc
		"""
		x, y = np.floor(self.ball_x * 12), np.floor(self.ball_y * 12)
		if self.ball_x >= 1:
			x = 12
		index = x + y * 12
		return (x, y), index

	def get_state(self):

		# State is calculate with 12x12 grid, x_vel (+-1), y_vel (+-1 or 0), and paddle_y (12 possible values)
		cell, cell_index = self.get_cell()
		if cell[0] = 12:
			return self_state.size - 1
		
		x_vel_index = [-1, 1].index(self.discrete_velocity_x)
		y_vel_index = [-1, 0, 1].index(self.discrete_velocity_y)
		state = np.floor(cell_index + 144 * x_vel_index )
		state = np.floor( ( (y_vel_index + 3 * self.discrete_paddle_y) * 2 + x_vel_index ) * 144 + cell_index )
		return state
		


g = Game()
g.convert_to_discrete()
print(g.get_state())