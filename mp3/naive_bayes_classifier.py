import numpy as np 
import math
import sys

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
		training_labels_location, test_data_location, test_labels_location, test_out_location):
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
		"""
		self.dim_x = dim_x
		self.dim_y = dim_y
		self.num_filler = num_filler
		self.classes = classes
		self.features = features
		self.dim_z = len(self.classes)
		self.laplace_v = laplace_v
		self.laplace_k = laplace_k
		self.training_data_location = training_data
		self.training_labels_location = training_labels_location
		self.test_data_location = test_data_location
		self.test_labels_location = test_labels_location
		self.test_out_location = test_out_location

		self.classifier = np.full((self.dim_x, self.dim_y, self.dim_z), self.laplace_k) # The 3D array representing likelihood estimators for each feature at (i, j)
		self.class_frequencies = np.full((1, dim_z), 0) # An array of prior frequencies for each class 
		self.class_probabilities = np.full((1, dim_z), math.inf) # An array of prior probabilities for each class. Separate from the above because the frequencies are used sometimes, so it's useful to be able to access both. 
			# Each class probability is initialized to infinity until they are updated to their proper values
		self.num_examples = 0 # The total number of training examples we read in 

	"""
	Lots of boilerplate for the useful getters and setters -_-
	"""
	def get_x(self):
		"""
		Returns the width of the input
		There is no associated setter. This is READ-ONLY.
		"""
		return self.dim_x

	def get_y(self):
		"""
		Returns the height of the input
		There is no associated setter. This is READ-ONLY.
		"""
		return self.dim_y

	def get_z(self):
		"""
		Returns the number of classes 
		There is no associated setter. This is READ-ONLY.
		"""
		return self.dim_z

	def get_feature_frequency(self, i, j, k):
		"""
		Returns the number of times a feature (i, j) has had F_ij == 1
		Only useful while the NBC is being trained; at the end of the training process, the frequencies are converted into probabilities
		"""
		if self.classifier[i, j, k] < 1:
			print("Feature frequencies have been converted to probabilities so this information is no longer useful")
			return 0
		else:
			return self.classifier[i, j, k]

	def increment_feature_frequency(self, i, j, k):
		"""
		Increments the number of times a feature (i, j) has had F_ij == 1
		Only useful while the NBC is being trained; at the end of the training process, the frequencies are converted into probabilities
		"""
		if self.classifier[i, j, k] < 1:
			print("Feature frequencies have been converted to probabilities so this information is no longer useful")
		else:
			self.classifier[i, j, k] += 1

	def get_class_frequency(self, k):
		"""
		Returns the number of times class k has appeared in the training examples
		For the inputs relevant to this MP, all classes will be integers
		If k IS an int, it should be zero-indexed
		Unlike feature frequencies, this is always a useful method because we maintain a separate list of class probabilities
		"""
		try:
			return self.class_frequencies[k]
		except IndexError:
			print("This class either does not exist, or it needs to be zero-index'd")
			return -1
	
	def get_feature_probability(self, i, j, k):
		"""
		Gets the probability of feature (i, j) having F_ij == 1
		Only useful after the NBC has been trained since the frequencies originally stored in the 3D array will be converted to probabilities
		"""
		if self.classificer[i, j, k] > 1:
			print("Feature frequencies have not been converted to probabilities so this information will not be useful")
			return -1
		else:
			return self.classifier[i, j, k]

	def increment_class_frequency(self, k):
		"""
		Increments the record of how many times class k has appeared in the training examples 
		For the inputs relevant to this MP, all classes will be integers 
		If k IS an int, it should be zero-indexed
		Unlike feature frequencies, this is always a useful method because we maintain a separate list of class probabilities
		"""
		try:
			self.class_frequencies[k] += 1
		except IndexError:
			print("This class either does not exist, or it needs to be zero-index'd")
		
	def get_class_probability(self, k):
		"""
		Returns the probability of class k appearing
		Only useful after training since we convert the class frequencies to probabilities at the end
		For the inputs relevant to this MP, all classes will be integers
		If k IS an int, it should be zero-indexed
		"""
		try:
			if self.class_probabilities[k] == math.inf:
				print("Class probabilities have not been updated yet (i.e., this NBC is still training")
				return -1
			else:
				return self.class_probabilities[k]
		except IndexError:
			print("This class either does not exist, or it needs to be zero-index'd")
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
					sample += TD.readline().strip()
				for j in range(self.num_filler):
					TD.readline()
				for j in range(self.dim_y):
					for i in range(self.dim_x):
						if self.features[sample[j * dim_x + i]] == 1:
							self.increment_feature_frequency(i, j, label)

	def convert_to_likelihoods(self):
		"""
		Converts the feature frequencies to probabilities
		"""
		for k in range(self.dim_z):
			denom = self.class_frequencies[k] + self.laplace_v + self.laplace_k
			for i in range(self.dim_x):
				for j in range(self.dim_y):
					self.classifier[i, j, k] /= denom

	def test_NBC(self):
		"""
		Tests the Naive Bayes Classifier by attempting to classify novel examples
		"""
		with open(self.test_data_location) as TD, open(self.test_out_location) as TO:
			while True:
				classifications = np.zeros(self.dim_z)
				for k in range(self.dim_z):
					classifications.append(math.log(self.get_class_probability(k)))
				sample = ""
				for j in range(self.dim_y):
					line = TD.readline()
					if line == "":
						break
					sample += line.strip()
				for j in range(self.num_filler):
					TD.readline()
				for j in range(self.dim_y):
					for i in range(self.dim_x):
						for k in range(self.dim_z):
							if self.features[sample[j * dim_x + i]] == 1:
								classifications[k] += math.log(self.get_feature_probability(i, j, k))
				max_index = 0
				max_val = -math.inf
				for k in range(dim_z):
					if classifications[k] > max_val:
						max_index = k
						max_val = classifications[k]
				TO.write("{0}\n".format(max_index))