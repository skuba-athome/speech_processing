import sys

if __name__ == "__main__":
	sentences = open(sys.argv[1], 'r')
	output = open(sys.argv[2], 'w')
	for sentence in sorted([ line.upper() for line in sentences.readlines()]):
		words = sentence.split()
		if len(words) is not 0:
			line = ""
			for word in words:
				line += word + ','
			output.write(line[:-1]+'\n')
	sentences.close()
	output.close()