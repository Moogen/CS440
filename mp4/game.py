import numpy as np
import random
import time

class Game:

	def __init__(self, num_train, num_games):

		#q learning stuff
		self.state_size = 10369
		self.Q = np.zeros([self.state_size, 3])
		self.learning_rate = 0.3
		self.discount_factor = 0.3
		self.epsilon = 0.05 	# chance that a random action is taken

		# game stuff
		self.num_train = num_train
		self.num_games = num_games
		self.num_bounces = 0
		self.num_games_played = -1

		self.restart()

	def restart(self):
		self.paddle_height = 0.2
		self.ball_x = 0.5
		self.ball_y = 0.5
		self.velocity_x = 0.03
		self.velocity_y = 0.01
		self.paddle_x = 1
		self.paddle_y = 0.5 - self.paddle_height / 2

		self.num_games_played += 1

	def start(self):
		start = time.time()
		while self.num_games_played < self.num_train:
			self.update()

		self.num_games_played = 0
		self.num_bounces = 0
		while self.num_games_played < self.num_games:
			self.update()

		print(self.num_bounces / self.num_games)
		print(self.num_bounces)
		print(time.time() - start)

	def update(self):
		self.convert_to_discrete()

		# Before updating values, get the old state first to calculate q values
		old_state = self.get_state()

		# Increment ball_x by velocity_x and ball_y by velocity_y
		self.ball_x += self.velocity_x
		self.ball_y += self.velocity_y

		# Check for bounces
		self.bounce()

		# update the Q matrix - this will also move the paddle
		self.calculate_Q(old_state)

		# If a player scored, restart the game
		if self.player_scored():
			self.restart()

	def bounce(self):
		# If ball_y < 0 (the ball is off the top of the screen), assign ball_y = -ball_y and velocity_y = -velocity_y
		if self.ball_y < 0:
			self.ball_y = -self.ball_y
			self.velocity_y = -self.velocity_y

		# If ball_y > 1 (the ball is off the bottom of the screen), let ball_y = 2 - ball_y and velocity_y = -velocity_y.
		if self.ball_y > 1:
			self.ball_y = 2 - self.ball_y
			self.velocity_y = -self.velocity_y

		# If ball_x < 0 (the ball is off the left edge of the screen), assign ball_x = -ball_x and velocity_x = -velocity_x.
		if self.ball_x < 0:
			self.ball_x = -self.ball_x
			self.velocity_x = -self.velocity_x

		# If moving the ball to the new coordinates resulted in the ball bouncing off the paddle, 
		# handle the ball's bounce by assigning ball_x = 2 * paddle_x - ball_x. Furthermore, when the ball bounces off a paddle, 
		# randomize the velocities slightly by using the equation velocity_x = -velocity_x + U and velocity_y = velocity_y + V, 
		# where U is chosen uniformly on [-0.015, 0.015] and V is chosen uniformly on [-0.03, 0.03]. 
		# As specified above, make sure that all |velocity_x| > 0.03.
		
		if self.ball_hit_paddle():
			self.ball_x = 2 * self.paddle_x - (self.ball_x + self.velocity_x)
			U, V = (0.015 - random.random() * 0.015 * 2), (0.03 - random.random() * 0.03 * 2)
			self.velocity_x = -self.velocity_x + U
			self.velocity_y = self.velocity_y + V
			self.num_bounces += 1

		if np.abs(self.velocity_x) < 0.03:
			self.velocity_x = 0.03 * np.sign(self.velocity_x)

	def ball_hit_paddle(self):
		x_i, y_i = self.ball_x, self.ball_y
		x_f, y_f = x_i + self.velocity_x, y_i + self.velocity_y

		if x_f < self.paddle_x:
			return False

		m = (y_f - y_i) / (x_f - x_i)
		b = y_i - m * x_i
		y_intersect = m * self.paddle_x + b

		if (y_intersect >= self.paddle_y) and (y_intersect <= self.paddle_y + self.paddle_height):
			return True

		return False

	def player_scored(self):
		if self.ball_x >= 1:
			return True
		else:
			return False


	### =================== Q LEARNING METHODS ==================== ###

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
		if self.ball_x <= 0:
			x = 0
		if self.ball_y >= 1:
			y = 11
		if self.ball_y <= 0:
			y = 0
		index = x + y * 12
		return (x, y), index

	def get_state(self):

		# State is calculate with 12x12 grid, x_vel (+-1), y_vel (+-1 or 0), and paddle_y (12 possible values)
		cell, cell_index = self.get_cell()
		if self.player_scored():
			return self.state_size - 1
		
		x_vel_index = [-1, 1].index(self.discrete_velocity_x)
		y_vel_index = [-1, 0, 1].index(self.discrete_velocity_y)
		state = np.floor( ( (3 * self.discrete_paddle_y + y_vel_index) * 2 + x_vel_index ) * 144 + cell_index )
		return int(state)

	def calculate_Q(self, old_state):
		actions = [-0.04, 0, 0.04]

		# First, choose an action
		action_index = 0
		v = self.Q[old_state]
		if random.random() < self.epsilon:
			action_index = int(random.random() * 3)
		else:
			#indices = [i for i, x in enumerate(v) if x == np.amax(v)]	# get all indices of the max values in Q[old_state]
			#action_index = random.choice(indices)
			action_index = np.argmax(self.Q[old_state])

		# Move the paddle
		self.paddle_y += actions[action_index]
		if self.paddle_y <= 0:
			self.paddle_y = 0
		if (self.paddle_y + self.paddle_height) >= 1:
			self.paddle_y = 1 - self.paddle_height

		# Calculate the reward
		r = 0
		self.convert_to_discrete()
		if self.ball_hit_paddle():
			r = 1
		if self.player_scored():		# out of bounds
			r = -1

		# calculate Q_max
		new_state = self.get_state()
		Q_max = max(self.Q[new_state])

		# update Q
		Q = self.Q[old_state, action_index]
		self.Q[old_state, action_index] = Q + self.learning_rate * (r + self.discount_factor * Q_max - Q)

		


g = Game(5000, 1)
g.start()