import numpy as np 
import math
import sys

# Laplace Smoothing Variables 
LAPLACE_K = 0
LAPLACE_V = 3

# Dimensions of the grid. Making a global variable on the off chance this can be adapted for part 2.
GRID_DIM = 28

class Grid:
	"""
	Represents the 28x28 grid of each image. 
	For every point (i, j), maintain an array of 10 floats: P(F_ij = foreground | C = c_k) is held at each index of the array.
	Three members: 
		Dimension: The NxN dimension of the board. 
		Class Probabilities: An array of size 10 that represents P(C = c_k) for k in [0, 9]
		Grid: The NxN board. Each point (i, j) on the board maintains an array of size 10. 
			Thus, a point (i, j, k) = P(F_ij = foreground | C = c_k)

	The grid initially holds the number of times we have seen a point (i, j) be foreground given a class c_k. This will be a whole number (duh).
	After all 5000 training sets have been examined, we will convert to a probability defined as follows:

										 	(# times F_ij was foreground given C = c_k) + LAPLACE_K
		P(F_ij = foreground | C = c_k) =   ---------------------------------------------------------
										 	      (# times C = c_k) + LAPLACE_K * LAPLACE_V	

	LAPLACE_K and LAPLACE_V are applied for Laplacian Smoothing 
	"""

	def __init__(self, dim):
		"""
		Initializes the class as defined above
		We will apply Laplacian smoothing anyway, so the initial frequency of each point (i, j, k) is set to LAPLACE_K
		"""
		self.dimension = dim
		self.class_probs = np.zeros(10)
		self.grid = np.full((self.dimension, self.dimension, 10), LAPLACE_K) # The starting frequency will just be k for convenience
	
	def __str__(self):
		"""
		Returns the string representation of the grid
		"""
		return "{0}".format(self.grid)

	def increment_feature_frequency(self, i, j, k):
		"""
		Numpy arrays are zero indexed so assume i and j start at 0
		"""
		self.grid[i, j, k] += 1

	def get_feature_frequency(self, i, j, k):
		"""
		Returns the value at point (i, j, k)
		"""
		return self.grid[i, j, k]

	def increment_class_frequency(self, k):
		self.class_probs[k] += 1

	def get_class_frequency(self, k):
		return self.class_probs[k]

	def get_dimension(self):
		return self.dimension

	def print_feature_frequency_by_class(self, k):
		out = ""
		for i in range(self.dimension):
			for j in range(self.dimension):
				out += str(self.grid[i, j, k])
				out += " "
			out += "\n"
		print("Feature frequencies for class {0}: {1}".format(k, out))

	def convert_to_likelihoods(self):
		for k in range(10):
			denom = self.class_probs[k] + LAPLACE_K * LAPLACE_V
			for i in range(self.dimension):
				for j in range(self.dimension):
					self.grid[i, j, k] /= denom
			self.class_probs[k] /= 5000 # 5000 training sets

def initialize(laplace_k):
	"""
	Initializes the digit objects
	"""
	global LAPLACE_K
	LAPLACE_K = float(laplace_k)
	grid = Grid(GRID_DIM)
	return grid
	
if __name__ == "__main__":
	initialize(5)