# word generator, given a set of legal letters

import enchant
from copy import copy

class Letter:
	def __init__(self, letters):
		'''constructor

		args:
			letters (list): List of possible letter.
		'''
		self.letters = letters

	def removeLetter(self, letter):
		try:
			self.letters.remove(letter)
		except ValueError:
			return False

	def setLetter(self, letter):
		self.letters = [letter]

	def getLetters(self):
		'''Returns all options for this letter, as a list of chars'''
		return self.letters

	def getLetter(self, index):
		'''Gets the letter with a given index.'''
		return self.letters[index] if index < len(self.letters) else None

class Word:
	def __init__(self, startWord, startLetters, unplacedLetters=[]):
		'''Constructor.
		
		For each letter in startWord, the letter is either set (if given), or unknown (if anything else).

		args:
			startWord (str or list): The word as yet determined, according to the description above.
			startLetters (str or list): The remaining valid letters.
			unplacedLetters (list): Letters that must appear at least once in the word.
		'''
		self.validLetters = [l for l in startLetters]
		self.unplacedLetters = [l for l in unplacedLetters]
		self.startWord = startWord
		self.letters = []
		self.d = enchant.Dict('en_US')
		for letter in startWord:
			l = Letter(copy(self.validLetters))
			if letter in 'abcdefghijklmnopqrstuvwxyz':
				l.setLetter(letter)
			self.letters.append(l)

	def isValidWord(self, word):
		'''Determines if the given word fits the constraints of the unplaced letters'''
		if word in self._found:
			return False
		for l in self.unplacedLetters:
			if l not in word:
				return False
		return self.d.check(word)
		
	def findOptions(self):
		'''Prints all options for the word, given current constraints'''
		self._found = ()
		maxes = [len(letter.getLetters()) for letter in self.letters]
		counts = [0 for i in range(len(maxes))]
		while counts[-1] < maxes[-1]-1:
			# print(counts)
			# print(maxes)
			# this is our "word creation" phase
			if counts[0] < maxes[0]:
				word = ''.join([self.letters[i].getLetter(counts[i]) for i in range(len(counts))])
				if self.isValidWord(word):
					self._found += (word,)
				counts[0] += 1
			else:
				# this is our "counting" phase
				counts[0] = 0
				j = 1
				counts[j] += 1
				while j < len(maxes) and counts[j] == maxes[j]:
					counts[j] = 0
					j += 1
					counts[j] += 1
		return self._found

	def printOptions(self):
		print(f'Possible words for {self.startWord}')
		print(f'Unplaced letters: {self.unplacedLetters}')
		print(f'Possible letters: {"".join(self.validLetters)}')
		print('-'*60)
		for option in self.findOptions():
			print(option)



if __name__ == '__main__':
	word = Word('..o..', 'roqwryioafjkzxvmg', '')
	# word.letters[0].removeLetter('r')
	# word.letters[3].removeLetter('a')
	# word.letters[3].removeLetter('a')
	word.printOptions()
