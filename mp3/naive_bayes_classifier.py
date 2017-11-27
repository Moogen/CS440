import numpy as np 
import math
import sys
from graphics import *

class NBC:
	"""
	A generic Naive Bayes Classifier for all parts of this mp.
	All training and testing inputs are given in text format. Let P be the width and Q be the height of each input. 
	Because of this format, the NBC takes the form of a 3-dimensional array of width P, height Q, and depth R.
		R is equal to the number of distinct classes there are. 
	Let 0 <= i < P, 0 <= j < Q, 0 <= k < R. 

	Every problem that this classifier is applied to can be defined in terms of classes, features, loss functions, and probabilities
		Classes: the set of identities that we want to assign to each test input. For example, "this input shows an 8" -> 8 is a class.
		Feature Set: the set of values that each point (i, j) can take on. A loss function F_ij is defined such that some of those values are considered 
			"good" (i.e., F_ij == 1) and some of the values are considered "bad" (i.e., F_ij == 0)
		Features: all points (i, j) in the input that will be used as prior likelihoods to influence what we think the test input's classification is. 
			There are a total of PxQ features.

	The point (i, j, k) in the array represents the likelihood of the function F_ij == 1 if we know the class is k. 
		That is, P(F_ij == 1 | class == c_k) 

	As is typical for supervised learning algorithms, this NBC will go through a training phase in which it reads in training images with associated labels. 
	The prior likelhiood at each point (i, j, k) will be adjusted as it is trained.
	After training, we can read in test images and attempt to classify them. 
	We then evaluate the success of the tests and generate accuracy data. 

	Predictions are done according to the Bayes Formula with the naive assumption that each feature influences the classification probability independently.
	We also apply Laplace Smoothing to account for cases where P(F_ij == 1 | class == c_k) == 0. Therefore,

								        (# times F_ij == 1 given C = c_k) + LAPLACE_K
		P(F_ij == 1 | C == c_k) = ---------------------------------------------------------
										 (# times C == c_k) + LAPLACE_K * LAPLACE_V	

	We also use logarithms for the maximum a priori decision to avoid underflow: 	
		P(C == c_k | F_00 AND F_01 AND ... F_ij for all i, j) = log(P(C == c_k)) + log(P(F_00 == 1 | C == c_k)) + ... log(P(F_ij == 1 | C == c_k))
	"""
	def __init__(self, dim_x, dim_y, num_filler, classes, features, laplace_v, laplace_k, training_data_location, 
		training_labels_location, test_data_location, test_labels_location, test_out_location, num_tests):
		"""
		Initializes a Naive Bayes Classifier object

		Arguments:
			dim_x: The width of the input
			dim_y: The height of the input 
			num_filler: The number of blank lines between consecutive text inputs
			classes: A list of the valid classes
			features: A dictionary of the feature values mapped to their loss function F_ij value (0 or 1)
			laplace_v: The value of V used for Laplace Smoothing
			laplace_k: The value of K used for Laplace Smoothing 
			training_data_location: The file location of the training data
			training_labels_location: The file location of the training labels
			test_data_location: The file location of the test data
			test_labels_location: The file location of the test labels. Obviously, only use this to compare results
			test_out_location: The file location that we want to put the output file when we test the classifier
			num_tests: The total number of test images this NBC will look at.
		"""
		self.dim_x = dim_x
		self.dim_y = dim_y
		self.num_filler = num_filler
		self.classes = classes
		self.features = features
		self.dim_z = len(self.classes)
		self.laplace_v = laplace_v
		self.laplace_k = laplace_k
		self.training_data_location = training_data_location
		self.training_labels_location = training_labels_location
		self.test_data_location = test_data_location
		self.test_labels_location = test_labels_location
		self.test_out_location = test_out_location

		self.classifier = np.full((self.dim_x, self.dim_y, self.dim_z), self.laplace_k) # The 3D array representing likelihood estimators for each feature at (i, j)
		self.class_frequencies = np.zeros(self.dim_z) # An array of prior frequencies for each class 
		self.class_probabilities = np.full(self.dim_z, math.inf) # An array of prior probabilities for each class. Separate from the above because the frequencies are used sometimes, so it's useful to be able to access both. 
			# Each class probability is initialized to infinity until they are updated to their proper values
		self.class_highest = np.full(self.dim_z, "")
		self.class_lowest = np.full(self.dim_z, "")
		self.num_examples = 0 # The total number of training examples we read in 
		self.num_tests = num_tests
		self.confusion_matrix = np.zeros((self.dim_z, self.dim_z))

	def __str__(self):
		"""
		Returns a string representation of the naive bayes classifier
		"""
		out = ""
		out += "Classifier dimensions: ({0}, {1}, {2})\n".format(self.dim_x, self.dim_y, self.dim_z)
		out += "Smoothing variables - V: {0}, K: {1}\n".format(self.laplace_v, self.laplace_k)
		out += "Class frequencies: {0}\n".format(self.class_frequencies)
		out += "Class probabilities: {0}\n".format(self.class_probabilities)
		out += "Total number of training examples: {0}\n".format(self.num_examples)
		for k in range(self.dim_z):
			out += "Likelihood Estimators of class {0}\n".format(k)
			for j in range(self.dim_y):
				for i in range(self.dim_x):
					out += "{0}  ".format(round(self.classifier[i, j, k], 3))
				out += "\n"
			out += "\n\n"
		return out

	def increment_feature_frequency(self, i, j, k):
		"""
		Increments the number of times a feature (i, j) has had F_ij == 1
		Only useful while the NBC is being trained; at the end of the training process, the frequencies are converted into probabilities
		"""
		if self.classifier[i, j, k] < 1 and self.laplace_k >= 1:
			print("Feature frequencies have been converted to probabilities so this information is no longer useful")
		else:
			self.classifier[i, j, k] += 1

	def get_feature_probability(self, i, j, k):
		"""
		Gets the probability of feature (i, j) having F_ij == 1
		Only useful after the NBC has been trained since the frequencies originally stored in the 3D array will be converted to probabilities
		"""
		if self.classifier[i, j, k] > 1:
			print("Feature frequencies have not been converted to probabilities so this information will not be useful")
			return -1
		else:
			return self.classifier[i, j, k]

	def get_class_frequency(self, k):
		"""
		Returns the number of times class k has appeared in the training examples
		For the inputs relevant to this MP, all classes will be integers
		Classes are not assumed to be zero-indexed
		Unlike feature frequencies, this is always a useful method because we maintain a separate list of class probabilities
		"""
		try: 
			return self.class_frequencies[self.classes.index(k)]
		except IndexError:
			print("This class does not exist")

	def increment_class_frequency(self, k):
		"""
		Increments the record of how many times class k has appeared in the training examples 
		For the inputs relevant to this MP, all classes will be integers 
		Classes are not assumed to be zero-indexed
		Unlike feature frequencies, this is always a useful method because we maintain a separate list of class probabilities
		"""
		try:
			self.class_frequencies[self.classes.index(k)] += 1
		except IndexError:
			print("This class does not exist")

	def get_class_probability(self, k):
		"""
		Returns the probability of class k appearing
		Only useful after training since we convert the class frequencies to probabilities at the end
		For the inputs relevant to this MP, all classes will be integers
		Classes are not assumed to be zero-indexed
		"""
		try:
			if self.class_probabilities[self.classes.index(k)] == math.inf:
				print("Class probabilities have not been updated yet (i.e., this NBC is still training")
				return -1
			else:
				return self.class_probabilities[self.classes.index(k)]
		except IndexError:
			print("This class does not exist")
			return -1
		
	def update_class_probabilities(self):
		"""
		Updates the class probabilities by dividing each class's frequencies by the total number of training examples
		"""
		for i in range(self.dim_z):
			self.class_probabilities[i] = self.class_frequencies[i] / self.num_examples

	def increment_num_examples(self):
		"""
		Increments the record of the number of training examples we have seen
		"""
		self.num_examples += 1

	def train_NBC(self):
		"""
		Trains the Naive Bayes Classifier 
		Reads in training data from the file at self.training_data_location and adjusts the likelihood estimators based on the 
			training labels found at training_labels_location 
		By the end, the NBC should have a dim_x X dim_y X dim_z array of bayesian likelihood estimators that can be used to classify novel examples.
		"""
		with open(self.training_data_location) as TD, open(self.training_labels_location) as TL:
			while True:
				label = TL.readline()
				if label == "":
					break
				label = int(label)
				self.increment_class_frequency(label)
				self.increment_num_examples()
				sample = ""
				for j in range(self.dim_y):
					sample += TD.readline().strip('\n')
				for j in range(self.num_filler):
					TD.readline()
				for j in range(self.dim_y):
					for i in range(self.dim_x):
						if self.features[sample[j * self.dim_x + i]] == 1:
							self.increment_feature_frequency(i, j, label)

	def convert_to_likelihoods(self):
		"""
		Converts the feature frequencies to probabilities
		"""
		for k in range(self.dim_z):
			denom = self.class_frequencies[k] + self.laplace_v * self.laplace_k
			for i in range(self.dim_x):
				for j in range(self.dim_y):
					self.classifier[i, j, k] /= denom

	def test_NBC(self):
		"""
		Tests the Naive Bayes Classifier by attempting to classify novel examples
		"""
		with open(self.test_data_location) as TD, open(self.test_out_location, 'w') as TO:
			for tests in range(self.num_tests):
				classifications = np.zeros(self.dim_z)
				for k in range(self.dim_z):
					classifications[k] += math.log(self.get_class_probability(self.classes[k]))
				sample = ""
				for j in range(self.dim_y):
					sample += TD.readline().strip('\n')
				for j in range(self.num_filler):
					TD.readline()
				for k in range(self.dim_z):
					for j in range(self.dim_y):
						for i in range(self.dim_x):
							if self.features[sample[j * self.dim_x + i]] == 1:
								classifications[k] += math.log(self.get_feature_probability(i, j, k))
							else:
								classifications[k] += math.log(1 - self.get_feature_probability(i, j, k))
				max_index = 0
				max_val = -math.inf
				for k in range(self.dim_z):
					if classifications[k] > max_val:
						max_index = k
						max_val = classifications[k]
				TO.write("{0}\n".format(max_index))

	def evaluate_accuracy(self):
		"""
		Evaluates how well the NBC did.
		Reports the performance in terms of the overall classification accuracy for each class as well as a confusion matrix. 
		For an arbitrary row r and column c, (r, c) in the confusion matrix is the percentage of test images from class r that are classified as class c.
		"""
		classification_frequency = np.zeros(self.dim_z)
		classification_total = np.zeros(self.dim_z)
		#confusion_matrix = np.zeros((self.dim_z, self.dim_z))

		with open(self.test_labels_location) as TL, open(self.test_out_location) as TO:
			for rem in range(self.num_tests):
				prediction = int(TO.readline())
				ground_truth = int(TL.readline())
				self.confusion_matrix[ground_truth, prediction] += 1
				if prediction == ground_truth:
					classification_frequency[self.classes.index(ground_truth)] += 1
					classification_total[self.classes.index(ground_truth)] += 1
				else: 
					classification_total[self.classes.index(ground_truth)] += 1
			for rem in range(classification_frequency.size):
				classification_frequency[rem] = classification_frequency[rem] / classification_total[rem]
				print("Class: {0}, Accuracy: {1}\n".format(rem, round(classification_frequency[rem], 3)))
			average = 0
			for rem in range(classification_frequency.size):
				average += classification_frequency[rem] 
			average /= classification_frequency.size

			for i in range(self.dim_z):
				total = np.sum(self.confusion_matrix[i])
				for j in range(self.dim_z):
					self.confusion_matrix[i, j] /= total
					self.confusion_matrix[i, j] = round(self.confusion_matrix[i, j], 3) * 100
			print("Overall accuracy: {0}\n".format(round(average, 3)))

			print("Confusion Matrix:")
			matrix = "\t"
			for k in range(self.dim_z):
				matrix += "{:<6}".format(self.classes[k])
			matrix += "\n"
			for i in range(self.dim_z):
				matrix += "{:<7}".format(self.classes[i])
				for j in range(self.dim_z):
					matrix += "{:^6}".format(round(self.confusion_matrix[j, i], 3))
				matrix += "\n"
			print(matrix)

	def get_largest(self, matrix):
		"""
		Returns the coordinate with the largest confusion rate in the matrix
		"""
		largest = -math.inf
		coord = (0, 0)
		for i in range(self.dim_z):
			for j in range(self.dim_z):
				if i == j:
					continue
				if matrix[j, i] > largest:
					largest = matrix[j, i]
					coord = (j, i)
		return coord

	def get_pairs(self):
		"""
		Returns the four pairs of digits that have the highest confusion rates according to the confusion matrix
		This could definitely be done better with sorting but whatever
		"""
		matrix = np.copy(self.confusion_matrix)
		pairs = []
		for i in range(4):
			pair = self.get_largest(matrix)
			pairs.append(pair)
			matrix[pair[0], pair[1]] = -math.inf
		return pairs

	def odd_ratios(self, pairs):
		"""
		Prints pretty pictures
		"""
		print("Four highest confusion pairs: {}".format(pairs))
		cell_size = 10
		windows = []
		for i in range(len(pairs) * 3):
			win = GraphWin('graphics', cell_size * self.dim_x, cell_size * self.dim_y)
			windows.append(win)
		index = 0
		for pair in pairs:
			c1, c2 = pair
			for i in range(self.dim_x):
				for j in range(self.dim_y):
					x, y = i * cell_size, j * cell_size
					f1 = math.log(self.classifier[i, j, c1])
					f2 = math.log(self.classifier[i, j, c2])
					odds = math.log(self.classifier[i, j, c1] / self.classifier[i, j, c2])

					# Feature Classifier 1
					color1 = 'firebrick'
					if f1 < -0.3:
						color1 = 'red'
					if f1 < -0.6:
						color1 = 'orange red'
					if f1 < -0.9:
						color1 = 'orange'
					if f1 < -1.2:
						color1 = 'yellow'
					if f1 < -1.5:
						color1 = 'pale green'
					if f1 < -1.8:
						color1 = 'aquamarine'
					if f1 < -2.1:
						color1 = 'deep sky blue'
					if f1 < -2.4:
						color1 = 'royal blue'
					if f1 < -2.7:
						color1 = 'blue'
					if f1 < -3:
						color1 = 'midnight blue'
					rect = Rectangle(Point(x, y), Point(x + cell_size, y + cell_size))
					rect.setOutline(color1)
					rect.setFill(color1)
					rect.draw(windows[index])

					# Feature Classifier 2
					color2 = 'firebrick'
					if f2 < -0.3:
						color2 = 'red'
					if f2 < -0.6:
						color2 = 'orange red'
					if f2 < -0.9:
						color2 = 'orange'
					if f2 < -1.2:
						color2 = 'yellow'
					if f2 < -1.5:
						color2 = 'pale green'
					if f2 < -1.8:
						color2 = 'aquamarine'
					if f2 < -2.1:
						color2 = 'deep sky blue'
					if f2 < -2.4:
						color2 = 'royal blue'
					if f2 < -2.7:
						color2 = 'blue'
					if f2 < -3:
						color2 = 'midnight blue'
					rect = Rectangle(Point(x, y), Point(x + cell_size, y + cell_size))
					rect.setOutline(color2)
					rect.setFill(color2)
					rect.draw(windows[index + 1])

					# Odd Ratio 	
					color_odds = 'firebrick'
					if odds < 1.5:
						color_odds = 'red'
					if odds < 1.:
						color_odds = 'orange red'
					if odds < 0.5:
						color_odds = 'orange'
					if odds < 0:
						color_odds = 'yellow'
					if odds < -0.5:
						color_odds = 'pale green'
					if odds < -1:
						color_odds = 'aquamarine'
					if odds < -1.5:
						color_odds = 'deep sky blue'
					if odds < -2:
						color_odds = 'royal blue'
					if odds < -2.5:
						color_odds = 'blue'
					if odds < -3:
						color_odds = 'midnight blue'
					rect = Rectangle(Point(x, y), Point(x + cell_size, y + cell_size))
					rect.setOutline(color_odds)
					rect.setFill(color_odds)
					rect.draw(windows[index + 2])
			index += 3
		for i in range(len(pairs) * 3):
			# Parallel where
			windows[i].getMouse()
			windows[i].getMouse()
			windows[i].close()