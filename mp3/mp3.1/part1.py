import numpy as np 
import math
import sys
from utils import *

# File paths
TRAINING_IMAGES = "../data/digit_data/trainingimages"
TRAINING_LABELS = "../data/digit_data/traininglabels"
TEST_IMAGES = "../data/digit_data/testimages"
TEST_LABELS = "../data/digit_data/testlabels"
TEST_OUT = "../data/digit_data/testout"
def train_NBC(grid):
	# Define i as horizontal and j as vertical. k indexes the array at each point (i, j), but can also be thought of as the z-axis

	with open(TRAINING_IMAGES) as TI, open(TRAINING_LABELS) as TL:
		for numSets in range(5000): 
			k = int(TL.readline())
			grid.increment_class_frequency(k)
			for j in range(grid.get_dimension()): 
				line = TI.readline()
				for i in range(grid.get_dimension()): 
					if line[i] == '+' or line[i] == '#':
						grid.increment_feature_frequency(i, j, k)
	grid.convert_to_likelihoods()

def test_NBC(grid):
	with open(TEST_OUT, 'w') as TO, open(TEST_IMAGES) as TI:
		for numSets in range(1000):
			classifications = []
			for k in range(10):
				classifications.append(math.log(grid.get_class_frequency(k)))
			for j in range(grid.get_dimension()):
				line = TI.readline()
				for i in range(grid.get_dimension()):
					for k in range(10):
						if line[i] == '+' or line[i] == '#':
							classifications[k] += math.log(grid.get_feature_frequency(i, j, k))
			max_index = 0
			max_val = -math.inf 
			for k in range(10):
				if classifications[k] > max_val:
					max_index = k
					max_val = classifications[k]
			TO.write("{0}\n".format(max_index))

def evaluate_accuracy():
	correct = 0
	total = 0
	with open(TEST_OUT) as TO, open(TEST_LABELS) as TL:
		for i in range(1000):
			NBC_answer = int(TO.readline())
			ground_truth = int(TL.readline())
			if NBC_answer == ground_truth:
				correct += 1
				total += 1
			else:
				total += 1
	return correct / total

def print_usage():
	print("To use:\npython part1.py [digit between 0.1 and 10]")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print_usage()
	else:
		grid = initialize(sys.argv[1])
		train_NBC(grid)
		test_NBC(grid)
		print("The Naive Bayes Classifier is {0} percent accurate".format(evaluate_accuracy()))