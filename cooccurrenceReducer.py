#!/usr/bin/env python

from operator import itemgetter
import sys

class Reducer():
	def __init__(self):
		self.combiner = {}

	def reduce(self):
		while True:
			line = sys.stdin.readline()
			if not line:
				break

			line = line.strip()

			word1, word2 = line.split('\t')
			word = word1 + ' ' + word2

			self.updateCombiner(word)

	def updateCombiner(self, key, count=1):
		'''this function updates the combiner dictionary for the given key'''

		if key in self.combiner:
			self.combiner.update({key:(self.combiner.get(key)+count)})
		else:
			self.combiner.update({key:count})

	def emitWords(self, outputStringFormat):
		for key, value in self.combiner.items():
			print outputStringFormat % (key, str(value))

if __name__ == '__main__':
	outputStringFormat = "{text:'%s', size:%s},"

	reducer = Reducer()
	reducer.reduce()
	reducer.emitWords(outputStringFormat)