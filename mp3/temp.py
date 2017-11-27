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
			