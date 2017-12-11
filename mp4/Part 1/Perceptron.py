'''
Created on Dec 10, 2017

@author: ZW
'''
import math
import csv
import random
import sys
from heapq import nlargest
from collections import Counter
import numpy as np

#globals
bigtrainingimg = [[] for y in range(5000)]
traininglabels = []
bigtestimg = [[] for y in range(1000)]
testlabels = []


#read training images
def readfiles(training_filename, training_label_filename, testing_filename, testing_label_filename):
	bigtrainingfile = open(training_filename)
	listcount = 0
	imgcount = 0
	for line in bigtrainingfile:
	    img_strings = list(line)
	    if (listcount == 28):
	        listcount = 0
	        imgcount = imgcount + 1
	    bigtrainingimg[imgcount].append(img_strings)
	    listcount = listcount + 1
	print("Done")

	#read training lines

	traininglabelfile = open(training_label_filename)
	for line in traininglabelfile:
	    traininglabels.append(line.split()[0])
	print("Done")
	    
	#read testimages

	bigtestfile = open(testing_filename)
	testlistcount = 0
	testimgcount = 0
	for line in bigtestfile:
	    img_strings = list(line)
	    if (testlistcount == 28):
	        testlistcount = 0
	        testimgcount += 1
	    bigtestimg[testimgcount].append(img_strings)
	    testlistcount += 1
	print("Done")

	#read test lines
	testlabelfile = open(testing_label_filename)
	for line in testlabelfile:
	    testlabels.append(line.split()[0])
	print("Done")

'''
k - initial weight values
b - bias
epoch - number of repetitions
learningrate - learning rate decay function
randomordering - fixed or random
'''
def adjust_weights(k, b, epoch, learningrate, randomordering):

	weights = [[[k for i in range(28)] for i in range(28)]for i in range(10)]
	accuracies = []
	if (randomordering == True):
		iterlist = random.sample(range(5000), 5000)
	else:
		iterlist = range(5000)

	for cycle in range(epoch):
	    accuracy = 0.0
	    for i in iterlist:
	        trainingclass = int(traininglabels[i])
	        #checks the weights in each training class
	        maxscore = float("-inf")
	        maxclass = 0
	        for j in range(10):
	            score = 0
	            for x in range(28):
	                for y in range(28):
	                    if (bigtrainingimg[i][x][y] == '#' or bigtrainingimg[i][x][y] == '+'):
	                        score += weights[j][x][y] * 1 + b 
	                    else:
	                        score += weights[j][x][y] * 0 + b
	            if (score > maxscore):
	                maxscore = score
	                maxclass = j
	        #update the weights if wrong
	        if (maxclass != trainingclass):
	            for x in range(28):
	                for y in range(28):
	                    if (bigtrainingimg[i][x][y] == '#' or bigtrainingimg[i][x][y] == '+'):
	                        weights[trainingclass][x][y] += (1 - learningrate * cycle)
	                        weights[maxclass][x][y] -= (1 - learningrate * cycle)
	        else:
	            accuracy += 1.0
	        
	    percent = accuracy / 5000.0
	    accuracies.append(str(accuracy) + "/5000")
	    print(str(accuracy) + "/5000")
	    iterlist = random.sample(range(5000), 5000)

	#Now that we have the correct weights on our training set, we can use them to classify our test set.
	return weights, accuracies
        
#classifying test digits
def classify_test(weights):
	testaccuracy = 0.0
	confusionmatrix = [[0 for i in range(10)] for i in range(10)]
	for i in range(1000):
	        testclass = int(testlabels[i])
	        #checks the weights in each training class
	        maxscore = float("-inf")
	        maxclass = 0
	        for j in range(10):
	            score = 0
	            for x in range(28):
	                for y in range(28):
	                    if (bigtestimg[i][x][y] == '#' or bigtestimg[i][x][y] == '+'):
	                        score += weights[j][x][y] * 1 + b 
	                    else:
	                        score += weights[j][x][y] * 0 + b
	            if (score > maxscore):
	                maxscore = score
	                maxclass = j
	        confusionmatrix[testclass][maxclass] += 1
	        if (maxclass == testclass):
	            testaccuracy += 1
	print(str(testaccuracy) + "/1000")
	return confusionmatrix, str(testaccuracy) + "/1000"
    
#calculate confusion matrix
def calculate_confusion_matrix(confusionmatrix):
	rowtotal = 0
	for i in range(10):
	    for j in range(10):
	        rowtotal += confusionmatrix[i][j]
	    for j in range(10):
	        confusionmatrix[i][j] = confusionmatrix[i][j]/float(rowtotal)
	    rowtotal = 0

	return confusionmatrix

#use nearest neighbor
def nearest_neighbor(k):
	confusionmatrix = [[0 for i in range(10)] for i in range(10)]
	accuracy = 0
	for i in range(len(bigtestimg)):
		guessed_class = get_neighbors(bigtestimg[i], k)
		actual_class = int(testlabels[i])

		if (guessed_class == actual_class):
			accuracy += 1
		confusionmatrix[actual_class][guessed_class] += 1
		if (i%50 == 0):
			print(i, guessed_class)
	print("Accuracy out of 1000:" + str(accuracy))
	return calculate_confusion_matrix(confusionmatrix)

#gets the k nearest neighbors for a specified test image and outputs the predicted class
def get_neighbors(testimage, k):
	pairs = []
	for i in range(5000):
		trainingimage = bigtrainingimg[i]
		trainingclass = int(traininglabels[i])

		dist = imagedistance(trainingimage, testimage)
		pairs.append([dist, trainingclass])
	knn = nlargest(k, pairs)

	classes = []
	for neighbor in knn:
		classes.append(neighbor[1])
	data = Counter(classes)
	commonclass = -1
	for nnclass, count in data.most_common(1):
		commonclass = nnclass
	return commonclass

def imagedistance(trainingimage, testimage):
	distance = 0
	for i in range(28):
		for j in range(28):
			if (trainingimage[i][j] == ' ' and testimage[i][j] == ' ') or (trainingimage[i][j] != ' ' and testimage[i][j] != ' '):
				distance += 1
	return distance

##Change to 1, 2, 3
def output_confusion_matrix(final_confusion_matrix, count):
	with open("cmatrix" + str(count) + ".csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(final_confusion_matrix)
def perceptron():
	weight_params = [[0,1,5,0.2,True]]
	count = 1
	for param in weight_params:
		k = param[0]
		b = param[1]
		epoch = param[2]
		learningrate = param[3]
		randomordering = param[4]

		print(k)
		print(b)
		print(epoch)
		print(learningrate)
		print(randomordering)

		weights, trainingaccuracies = adjust_weights(k, b, epoch, learningrate, randomordering)
		confusionmatrix, testaccuracy = classify_test(weights)
		final_confusion_matrix = calculate_confusion_matrix(confusionmatrix)

		with open("accuracies" + str(count) + ".txt", "w") as file:
			file.write("Training Accuracies \n")
			for item in trainingaccuracies:
				file.write("%s\n" % item)
			file.write("Testing Accuracies \n")
			file.write(testaccuracy)
		output_confusion_matrix(final_confusion_matrix)
		count += 1

readfiles("trainingimages", "traininglabels", "testimages", "testlabels")

for i in range(3,10,2):
	print("K: " + str(i))
	cm = nearest_neighbor(i)
	output_confusion_matrix(cm, i)