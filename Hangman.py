import Automate, ModDict, sys
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from HangmanInputProcessor import HangmanInputProcessor

class Hangman:
	def __init__(self,getAvg=False):
		self.weighted_list = []
		self.fill_factor_list = []
		self.indices_list = []
		self.toAvg = False
		self.TRIES = 6
		self.res_list = None

		if getAvg:
			self.toAvg = True

		self.setupGraphViz()
		self.rerunGame()

	def setupGraphViz(self):
		#run the code below whether or not the module is imported or run directly
		self.graphviz = GraphvizOutput()
		self.graphviz.output_file = 'flow_graph.png'
		with PyCallGraph(output=self.graphviz):
			isPassed = ModDict.loadAllDicts()
			if not isPassed:
				sys.exit("File not found in current directory")


	def rerunGame(self):
		self.Inp = HangmanInputProcessor(self.toAvg)
		self.runGame()

	def runGame(self):
		self.res_list = []
		self.TRIES = 3
		Automate.clearAll()
		self.weighted_list = [None] * len(self.Inp.split_input_list)

		self.weighted_list = map(lambda x: list(ModDict.modDict.get(str(len(x)))), self.Inp.split_input_list)
		Automate.calculateLetterWeightOfList(self.weighted_list, True)

		self.fill_factor_list = [0] * len(self.Inp.split_input_list)
		self.indices_list = [[]] * len(self.Inp.split_input_list)

		self.initializeState()
		if not self.toAvg: self.printState()
		self.playGame()

	def printState(self):
		print ("".join(self.res_list)) + "\n"

	def displayStats(self):
		print "\nTRIES LEFT:", str(self.TRIES) + " out of 3\n"

	def initializeState(self):
		list_len = reduce(lambda x,y: x + y, map(len,self.Inp.split_input_list)) + \
			(len(self.Inp.split_input_list) - 1)

		self.res_list = ["_"] * list_len

		#insert spaces
		inc = 0
		for x in self.Inp.split_input_list:
			inc += len(x)
			if inc < len(self.res_list):
				self.res_list[inc] = " "
				inc += 1

	def playGame(self):
		while self.TRIES != 0:
			ret = self.updateState() #retrieve the highest probablistic character
			if not self.toAvg: self.printState()
			if (ret == 1 or (ret == -1 and self.TRIES == 0)):
				if not self.toAvg:
					if ret == -1:
						print "DEAD -- Game Over"
					else:
						print "ALL COMPLETED! SOLVED!"
					self.displayStats()
					self.rerunGame()
				break

			#if only our guess was correct
			#if any(self.weighted_list):
			if len(Automate.sortedList) == 0 or (Automate.sortedList[-1][0] != 2 \
				and Automate.sortedList[-1][0] != 1.5):
					Automate.calculateLetterWeightOfList(self.weighted_list,False)

	def updateState(self):
		prev_inc = 0
		letter_found = 0

		guess = Automate.popMaxWeightChar()

		if not self.toAvg: print "Guess:", guess

		if (guess != None):
			guess = guess.lower()

			for index,word in enumerate(self.Inp.split_input_list):
				if self.fill_factor_list[index] == 1.0:
					prev_inc += len(word) + 1
					continue

				idx_list = [x for x,val in enumerate(word) if val == guess]
				#merge lists
				self.indices_list[index] = self.indices_list[index] + idx_list

				for x in idx_list:
					self.res_list[prev_inc + x] = guess

				if (len(idx_list) > 0):
					#our guess was correct
					letter_found |= 1

					temp_weighted_list = []

					for i in self.weighted_list[index]:
						idx_matches = 1
						for idx_num in idx_list:
							if i[idx_num] == guess:
								idx_matches &= 1
							else:
								idx_matches &= 0
								break
						if (idx_matches):
							temp_weighted_list.append(i)

					self.weighted_list[index] = temp_weighted_list

					#add for fill factor of each word
					self.fill_factor_list[index] = len(self.indices_list[index])/float(len(word))

					#we found the word; now we pick the letters in the word as our next guesses
					if len(self.weighted_list[index]) == 1 and self.fill_factor_list[index] < 1:
						Automate.prepForValidFoundSet(set(self.weighted_list[index][0]))

				else:
					#character we guessed was not in any of the words
					letter_found |= 0

					#remove characters in the list that don't match
					for i in self.weighted_list[index]:
						if guess in i:
							self.weighted_list[index].remove(i)

				prev_inc += len(word) + 1 #account for space
		else:
			print "no guess"
			if not self.toAvg:
				print "Cannot generate any more guesses."
				self.rerunGame()

		not_filled_list = [i for i,val in enumerate(self.fill_factor_list) if val < 1]

		#there is no point of picking word with highest frequency if the
		#word was chosen randomly by generator
		dirty_list = [x for i,x in enumerate(self.indices_list) if len(self.Inp.split_input_list[i]) - len(x) <= 2]
		if self.Inp.input_choice != "1" and len(dirty_list) == 0 and len(not_filled_list) !=0:
			if len(Automate.sortedList) == 0 or Automate.sortedList[-1][0] != 2:
				#all chars are distinct at this condition, so look for word frequency
				for x in not_filled_list:
					idxLeft = set(range(len(self.Inp.split_input_list[x]))) - set(self.indices_list[x])
					if len(idxLeft) > 0:
						idxLeft = idxLeft.pop()
						maxFreqSet = Automate.createWordFreqSortedList(self.weighted_list[x])
						Automate.addMostUniqueCharToList(maxFreqSet[-1][1][idxLeft])


		if len(not_filled_list) == 0:
			return 1

		if (letter_found == 0):
			self.TRIES -= 1
			if not self.toAvg: self.displayStats()
			return -1

		return 0


if __name__=='__main__':
	Hangman()
