from naive_bayes_classifier import * 

# File paths

# Digit file paths
DIGIT_TRAINING_IMAGES = "data/digit_data/trainingimages"
DIGIT_TRAINING_LABELS = "data/digit_data/traininglabels"
DIGIT_TEST_IMAGES = "data/digit_data/testimages"
DIGIT_TEST_LABELS = "data/digit_data/testlabels"
DIGIT_TEST_OUT = "data/digit_data/testout"

# Yes/No file paths
YESNO_TRAINING_IMAGES = ""


def print_usage():
	print("To use:\npython mp_main [1.1 | 1.2 | 1_ec | 2.1 | 2.2 | 2_ec] [value of laplace_k between 0.1 and 10]")

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print_usage()
	else:
		# Something