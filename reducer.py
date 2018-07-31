#!/usr/bin/env python

from operator import itemgetter
import sys

def singleWordCountReducer():
	outputStringFormat = "{text:\"%s\", size:%s},"

	current_word = None
	current_count = 0
	word = None

	while True:
	#for line in sys.stdin:
		line = sys.stdin.readline()
		if not line:
			break

		line = line.strip()

		word, count = line.split('\t')

		try:
			count = int(count)
		except ValueError:
			continue

		if current_word == word:
			current_count += count
		else:
			if current_word:
				print outputStringFormat % (current_word, current_count)
				# print '%s\t%s' % (current_word, current_count)

			current_count = count
			current_word = word

	if current_word == word:
		print outputStringFormat % (current_word, current_count)

if __name__ == '__main__':
	singleWordCountReducer()