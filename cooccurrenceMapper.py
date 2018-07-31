#!/usr/bin/env python

'''
1. removed stop words
2. lemmatizing of words
3. combiner implementation for each line
'''
import sys
import argparse

import nltk
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.stem import WordNetLemmatizer

import re

class Mapper:
	'''Mapper class, implementing mapper logic for cooccurrence of words'''

	def cooccurrenceMapper(self, cooccurrenceList):
		'''Mapper function to emit cooccurrence count'''

		# iterate over all the lines in the stdin
		for line in sys.stdin:
			# split line into formatted words
			words = formatInputWords(line)

			# iterate over list of cooccurrenceList words
			# outer loop iterates till cooccurrenceList[:-1]
			# inner loop iterates over cooccurrenceList[i+1:]
			for i in range(len(cooccurrenceList) - 1):
				for j in range(i+1, len(cooccurrenceList)):
					# if the words are in paragraph then they are
					# cooccurring
					if cooccurrenceList[i] in words and cooccurrenceList[j] in words:
						print '%s\t%s' % (cooccurrenceList[i], cooccurrenceList[j])

def formatInputWords(line):
	# lemmatizing object
	lemmatizer = WordNetLemmatizer()
	# remove leading and trailing whitespaces
	line = line.strip()
	# split the line into list of words
	words = line.split()
	# convert to ascii encoding
	words = [unicode(word, errors='ignore').encode('ascii') \
			 for word in words]
	# remove leading and trailing symbols from words
	words = [removeLeadingAndTrailingSymbolsFromWord(word) \
			 for word in words]
	# lemmatize words
	words = [(lemmatizer.lemmatize(word)).lower() for word in words]

	return words

def removeLeadingAndTrailingSymbolsFromWord(word):
	'''this function formats the words in the input line to a standard format'''
	
	# compile a pattern to check if word contains
	# .,!?') at its end'
	symbolPatternAtEnd = re.compile("[\+\=\[_/\@\*\$\&\#\.,!?'\(\)\]\}%\":;><|\-0-9]*$")
	symbolPatternAtStart = re.compile("^[\+\=\[_/\@\*\&\$\#\.,!?'\(\)\]\}%\":;><|\-0-9]*")
	# remove punctuation at the end of the word if any
	s = re.findall(symbolPatternAtEnd, word)[0]
	if len(s) > 0:
		word = word[:-1 * (len(s))]
	# remove punctuation at the start of the word if any
	s = re.findall(symbolPatternAtStart, word)[0]
	if len(s) > 0:
		word = word[len(s):]

	return word

def updateStopWords():
	'''this function is used to update the stop words corpus'''
	
	# adding couple of stop words
	STOP_WORDS.add("i'm")
	STOP_WORDS.add("isn't")
	STOP_WORDS.add("let's")
	STOP_WORDS.add("ha")
	STOP_WORDS.add("according")
	STOP_WORDS.add("want")
	STOP_WORDS.add("like")

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('-f', '--filepath', required=True,
		help='file path of the top ten words')
	args = vars(ap.parse_args())

	with open(args['filepath'], 'r') as f:
		lines = f.readlines()

	cooccurrenceList = [word.strip() for word in lines]
	
	updateStopWords()

	mapper = Mapper()
	mapper.cooccurrenceMapper(cooccurrenceList)
	mapper.emitWords()

'''
hadoop jar /home/hadoop/hadoop/contrib/hadoop-streaming-2.6.0.jar -file cooccurrenceMapper.py -file reducer.py -file top10wordsTwitter.txt -mapper './cooccurrenceMapper.py -f ./top10wordsTwitter.txt' -reducer reducer.py -input tweets_small_data -output tweets_small_data_cooccurrence
'''