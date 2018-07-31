#!/usr/bin/env python

'''
1. removed stop words
2. lemmatizing of words
3. combiner implementation for each line
'''

import sys

import nltk
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.stem import WordNetLemmatizer

import re

def singleWordCountMapper():
	# list of stop words
	# stopwordsList = stopwords.words('english')

	# lemmatizing object
	lemmatizer = WordNetLemmatizer()

	# compile a pattern to check if word contains
	# .,!?') at its end'
	symbolPatternAtEnd = re.compile("[\+\=\[_/\@\*\$\&\#\.,!?'\(\)\]\}%\":;><|\-0-9]*$")
	symbolPatternAtStart = re.compile("^[\+\=\[_/\@\*\&\$\#\.,!?'\(\)\]\}%\":;><|\-0-9]*")

	# combiner dictionary
	# structure to imitate associative array
	combiner = {}

	# iterate over all the lines in the stdin
	for line in sys.stdin:

		# remove leading and trailing whitespaces
		line = line.strip()

		# split the line into list of words
		words = line.split()

		# convert to ascii encoding
		words = [unicode(word, errors='ignore').encode('ascii') \
				 for word in words]

		for word in words:
			# convert to ascii encoding
			# word = unicode(word, errors='ignore').encode('ascii')

			# remove punctuation at the end of the word if any
			s = re.findall(symbolPatternAtEnd, word)[0]
			if len(s) > 0:
				word = word[:-1 * (len(s))]

			# remove punctuation at the start of the word if any
			s = re.findall(symbolPatternAtStart, word)[0]
			if len(s) > 0:
				word = word[len(s):]

			# lemmatize the word
			wordLemma = (lemmatizer.lemmatize(word)).lower()

			# if the word is not in stop words list and not hyperlinks
			if not wordLemma in STOP_WORDS and not wordLemma[:5] == 'https':
				# add word to combiner dictionary
				# if word is already present in dictionary
				# then increment the count
				if wordLemma in combiner:
					count = combiner.get(wordLemma) + 1
					combiner.update({wordLemma:count})
				# if word is not present in dictionary then
				# add the word with count 1
				else:
					combiner.update({wordLemma:1})
		
	# emit word counts from combiner
	for word in combiner.keys():
		if len(word.strip()) > 0:
			print '%s\t%s' % (word, combiner.get(word))

if __name__ == '__main__':
	singleWordCountMapper()