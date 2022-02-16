# word generator, given a set of legal letters

import enchant
from copy import copy

class Letter:
	'''Stores a single letter object, including all possible values the letter can have.'''
	def __init__(self, letters):
		'''Constructor.

		Args:
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
	'''Stores a set of letters representing a state of the Wordle board.'''
	def __init__(self, startWord, startLetters, unplacedLetters=[]):
		'''Constructor.
		
		For each letter in startWord, the letter is either set (if given), or unknown (if anything else).

		args:
			startWord (str or list): The word as yet determined, according to the description above.
			startLetters (str or list): The remaining valid letters.
			unplacedLetters (list): Letters that must appear at least once in the word. Optional, empty by default.
		'''
		self.validLetters = [l for l in startLetters]
		self.unplacedLetters = [l for l in unplacedLetters]
		self.startWord = startWord
		self.letters = []
		self._found = None
		self.d = enchant.Dict('en_US')
		for letter in startWord:
			l = Letter(copy(self.validLetters))
			if letter in 'abcdefghijklmnopqrstuvwxyz':
				l.setLetter(letter)
			self.letters.append(l)

	def isValidWord(self, word):
		'''Determines if the given word fits the constraints of the unplaced letters.
	
		Also filters for repeats.

		Args:
			word (str): The word to check.

		Returns:
			bool: Whether the word is a valid word in US English, and also not already in self._found.
		'''
		if word in self._found:
			return False
		for l in self.unplacedLetters:
			if l not in word:
				return False
		return self.d.check(word)
		
	def findOptions(self):
		'''Finds all options for the word, given current constraints, and puts them in self._found.

		Note that results are filtered to avoid repeats, but not cached, so if you run this twice
		it'll take just as long the second time (sorry lol).

		Returns:
			tuple: The words possible from the given state.
		'''
		self._found = ()
		maxes = [len(letter.getLetters()) for letter in self.letters]
		counts = [0 for i in range(len(maxes))]
		while counts[-1] < maxes[-1]-1:
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
		'''Prints all options for the given state of the board, along with a bit of context.

		This calls self.findOptions(), and so takes just as long as that function.
		'''
		print(f'Possible words for {self.startWord}')
		print(f'Unplaced letters: {self.unplacedLetters}')
		print(f'Possible letters: {"".join(self.validLetters)}')
		print('-'*60)
		for option in self.findOptions():
			print(option)


# example: you've already guessed a couple times, and you've determines that the third letter is 'o',
#   'a' and 'r' are both in the word, 'a' can't be the 4th letter, and 'r' can't be the first or
#    fourth letters (this description is 1-indexed; the code is 0-indexed). The following creates a
#    wordle game state where the first arg is the word, with undetermined letters represented as dots,
#    the second arg is the remaining unguessed letters on the board, and the third arg is the set
#    of letters that are in the word but without a known location. Based on where these letters have
#    been found, we can eliminate them from the guesses for specific letters in the word; this is
#    what the following "removeLetter" lines do. Then we run the thing and get results printed.

# If you're curious, this is based on the 2/15 NYT wordle, with the solution (and only remaining
#    word) being "aroma".
if __name__ == '__main__':
	word = Word('..o..', 'roqwryioafjkzxvmg', '')
	word.letters[0].removeLetter('r')
	word.letters[3].removeLetter('a')
	word.letters[3].removeLetter('a')
	word.printOptions()