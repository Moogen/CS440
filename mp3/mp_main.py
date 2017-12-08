from naive_bayes_classifier import * 

# File paths

# Digit file paths
DIGIT_TRAINING_IMAGES = "data/digit_data/training_images.txt"
DIGIT_TRAINING_LABELS = "data/digit_data/training_labels.txt"
DIGIT_TEST_IMAGES = "data/digit_data/test_images.txt"
DIGIT_TEST_LABELS = "data/digit_data/test_labels.txt"
DIGIT_TEST_OUT = "data/digit_data/test_out.txt"
DIGIT_NUM_TESTS = 1000

# Face file paths
FACE_TRAINING_IMAGES = "data/face_data/training_images.txt"
FACE_TRAINING_LABELS = "data/face_data/training_labels.txt"
FACE_TEST_IMAGES = "data/face_data/test_images.txt"
FACE_TEST_LABELS = "data/face_data/test_labels.txt"
FACE_TEST_OUT = "data/face_data/test_out.txt"
FACE_NUM_TESTS = 150

# Yes/No file paths
YESNO_TRAINING_IMAGES = "data/yesno/training_images.txt"
YESNO_TRAINING_LABELS = "data/yesno/training_labels.txt"
YESNO_TEST_IMAGES = "data/yesno/test_images.txt"
YESNO_TEST_LABELS = "data/yesno/test_labels.txt"
YESNO_TEST_OUT = "data/yesno/test_out.txt"
YESNO_NUM_TESTS = 100

# Audio Digits file paths 
AD_TRAINING_IMAGES = "data/data22/training_images.txt"
AD_TRAINING_LABELS = "data/data22/training_labels.txt"
AD_TEST_IMAGES = "data/data22/test_images.txt"
AD_TEST_LABELS = "data/data22/test_labels.txt"
AD_TEST_OUT = "data/data22/test_out.txt"
AD_NUM_TESTS = 40

def digit_classifier(laplace_k):
	dim_x = 28
	dim_y = 28
	num_filler = 0
	classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	features = {' ' : 0, '+' : 1, '#' : 1}
	laplace_v = len(features.keys())
	NBC_digits = NBC(dim_x, dim_y, num_filler, classes, features, laplace_v, laplace_k, DIGIT_TRAINING_IMAGES, DIGIT_TRAINING_LABELS, 
		DIGIT_TEST_IMAGES, DIGIT_TEST_LABELS, DIGIT_TEST_OUT, DIGIT_NUM_TESTS)
	NBC_digits.train_NBC()
	NBC_digits.convert_to_likelihoods()
	NBC_digits.update_class_probabilities()
	NBC_digits.test_NBC()
	NBC_digits.print_prototypical()
	NBC_digits.evaluate_accuracy()
	pairs = NBC_digits.get_pairs()
	NBC_digits.odds_ratios(pairs)

def mp1_2(laplace_k):
	pass

def face_classifier(laplace_k):
	dim_x = 60
	dim_y = 70
	num_filler = 0
	classes = [0, 1]
	features = {' ' : 0, '#' : 1}
	laplace_v = len(features.keys())
	NBC_faces = NBC(dim_x, dim_y, num_filler, classes, features, laplace_v, laplace_k, FACE_TRAINING_IMAGES, FACE_TRAINING_LABELS, 
		FACE_TEST_IMAGES, FACE_TEST_LABELS, FACE_TEST_OUT, FACE_NUM_TESTS)
	NBC_faces.train_NBC()
	NBC_faces.convert_to_likelihoods()
	NBC_faces.update_class_probabilities()
	NBC_faces.test_NBC()
	NBC_faces.evaluate_accuracy()

def yesno_classifier(laplace_k):
	dim_x = 10
	dim_y = 25
	num_filler = 3
	classes = [0, 1]
	features = {'%' : 0, ' ' : 1}
	laplace_v = len(features.keys())
	NBC_yesno = NBC(dim_x, dim_y, num_filler, classes, features, laplace_v, laplace_k, YESNO_TRAINING_IMAGES, YESNO_TRAINING_LABELS,
		YESNO_TEST_IMAGES, YESNO_TEST_LABELS, YESNO_TEST_OUT, YESNO_NUM_TESTS)
	NBC_yesno.train_NBC()
	NBC_yesno.convert_to_likelihoods()
	NBC_yesno.update_class_probabilities()
	NBC_yesno.test_NBC()
	NBC_yesno.evaluate_accuracy()
	
# This definitely does not work right now but I don't have time to fix it 
def audio_digit_classifier(laplace_k):
	# NBC accuracy for this is legit 0
	# Figure out why......
	dim_x = 13
	dim_y = 30
	num_filler = 3
	classes = [1, 2, 3, 4, 5]
	features = {'%' : 0, ' ': 1}
	laplace_v = len(features.keys())
	NBC_ad = NBC(dim_x, dim_y, num_filler, classes, features, laplace_v, laplace_k, AD_TRAINING_IMAGES, AD_TRAINING_LABELS,
		AD_TEST_IMAGES, AD_TEST_LABELS, AD_TEST_OUT, AD_NUM_TESTS)
	NBC_ad.train_NBC()
	NBC_ad.convert_to_likelihoods()
	NBC_ad.update_class_probabilities()
	NBC_ad.test_NBC()
	NBC_ad.evaluate_accuracy()

def mp2_ec(laplace_k):
	pass

def print_usage():
	print("To use:\npython mp_main [1_1 | 1_2 | 1_ec | 2_1 | 2_2 | 2_ec] [value of laplace_k between 0.1 and 10]")

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print_usage()
	elif sys.argv[1] == "1_1":
		digit_classifier(float(sys.argv[2]))
	elif sys.argv[1] == "1_ec":
		face_classifier(float(sys.argv[2]))
	elif sys.argv[1] == "2_1":
		yesno_classifier(float(sys.argv[2]))
	elif sys.argv[1] == "2_2":
		audio_digit_classifier(float(sys.argv[2]))