from random import randint
import Automate, ModDict, sys
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

MAX_WORDS = 10 #default
MIN_WORDS = 1
MAX_STR_LEN = 15 #largest len found in dictionary provided
TRIES = 3
input_choice = 0
split_input_list = []
weighted_list = []
fill_factor_list = []
indices_list = []


def playGame():

	global TRIES
	while TRIES != 0:
		ret = updateState() #retrieve the highest probablistic character
		printState()
		if (ret == 1 or (ret == -1 and TRIES == 0)):
			if ret == -1:
				print "DEAD -- Game Over"
			else:
				print "ALL COMPLETED! SOLVED!"
			displayStats()
			rerunGame()
			break

		#if only our guess was correct
		#if any(weighted_list):
		if len(Automate.sortedList) == 0 or (Automate.sortedList[-1][0] != 2 \
			and Automate.sortedList[-1][0] != 1.5):
				Automate.calculateLetterWeightOfList(weighted_list,False)

def printState():
	
	print ("".join(res_list)) + "\n"
	
def displayStats():
	print "\nTRIES LEFT:", str(TRIES) + " out of 3\n"

def initializeState():
	list_len = reduce(lambda x,y: x + y, map(len,split_input_list)) + \
		(len(split_input_list) - 1)

	global res_list

	res_list = ["_"] * list_len

	#insert spaces 
	inc = 0
	for x in split_input_list:
		inc += len(x)
		if inc < len(res_list): 
			res_list[inc] = " "
			inc += 1
	
def binarySearch(word,wordList):

	list_len = len(wordList)
	if (list_len == 0): 
		return False
	
	mid = list_len/2
	chosenWord = wordList[mid].lower()
	if (chosenWord == word): 
		return True
	elif chosenWord > word:
		return binarySearch(word,wordList[:mid])
	elif chosenWord < word:
		return binarySearch(word,wordList[mid+1:])


def generate_input():
	ret_list = []
	word_num = randint(MIN_WORDS,MAX_WORDS)
	for rang in range(word_num):
		
		str_len = str(randint(MIN_WORDS,MAX_STR_LEN))
		while (str_len not in ModDict.modDict):
			str_len = str(randint(MIN_WORDS,MAX_STR_LEN))
		
		array = ModDict.modDict.get(str_len)
		chosen_word = array[randint(0,len(array) - 1)]
		ret_list.append(chosen_word.lower())
	return ret_list

def requireInput():
	while (True):
		str_input = raw_input("--> Enter input: ")
		global split_input_list
		split_input_list = str_input.lower().split()
		if len(split_input_list) > MAX_WORDS: 
			print "Maximum string length is 10\n"
			continue

		dirty_list = filter(lambda x: binarySearch(x, ModDict.modDict.get(str(len(x)))) == 0,\
			split_input_list)
	
		if (len(dirty_list) != 0):
			print "The following words are not found in the dictionary:",\
				",".join(dirty_list), ". Re-enter input.\n"
		else:
			print "Entered Input:", " ".join(split_input_list)
			break

def preProcessor():
	global split_input_list,input_choice

	while (True):
		print "1 : Generate input for me"
		print "2 : Enter custom input"
		print "Type 'out' to exit program"

		try: 
			input_choice = raw_input("--> ")
			
			if input_choice == "1":
				#list of strings
				split_input_list = generate_input()
				print "Generated Input:", " ".join(split_input_list)
				break

			elif input_choice == "2":
				requireInput()
				break
			elif input_choice == "out":
				sys.exit(0)
			else:
				print "Not a possible option\n"
		except Exception,e:
			print "Error:", str(e)

def updateState():

	global TRIES

	prev_inc = 0
	letter_found = 0

	guess = (Automate.popMaxWeightChar()).lower()

	print "Guess:", guess

	if (guess != None):
		for index,word in enumerate(split_input_list):

			if fill_factor_list[index] == 1.0:
				prev_inc += len(word) + 1 
				continue

			idx_list = [x for x,val in enumerate(word) if val == guess]
			
			#merge lists
			indices_list[index] = indices_list[index] + idx_list
			for x in idx_list:
				res_list[prev_inc + x] = guess

			
			if (len(idx_list) > 0):

				#our guess was correct
				letter_found |= 1
			
				temp_weighted_list = []

				for i in weighted_list[index]:
					idx_matches = 1
					for idx_num in idx_list:
						if i[idx_num] == guess:
							idx_matches &= 1
						else:
							idx_matches &= 0
							break
					if (idx_matches):
						temp_weighted_list.append(i)

				weighted_list[index] = temp_weighted_list

				#add for fill factor of each word
				fill_factor_list[index] = len(indices_list[index])/float(len(word))

				#we found the word; now we pick the letters in the word as our next guesses
				if len(weighted_list[index]) == 1:
					Automate.prepForValidFoundSet(set(weighted_list[index][0]))
					
			else:
				#character we guessed was not in any of the words
				letter_found |= 0

				#remove characters in the list that don't match
				for i in weighted_list[index]:
					if guess in i:
						weighted_list[index].remove(i)


			prev_inc += len(word) + 1 #account for space
	else:
		print "Cannot generate any more guesses. Crash!"
		rerunGame()

	not_filled_list = [i for i,val in enumerate(fill_factor_list) if val < 1]

	#there is no point of picking word with highest frequency if the 
	#word was chosen randomly by generator
	dirty_list = [x for x in indices_list if len(word) - len(x) > 2]
	if input_choice != "1" and len(dirty_list) == 0 and len(not_filled_list) !=0:
		if len(Automate.sortedList) == 0 or Automate.sortedList[-1][0] != 2:
			#all chars are distinct at this condition, so look for word frequency
			for x in not_filled_list:
				idxLeft = set(range(len(word))) - set(indices_list[index])
				if len(idxLeft) > 0:
					idxLeft = idxLeft.pop()
					maxFreqSet = Automate.createWordFreqSortedList(weighted_list[x])
					Automate.sortedList.add((1.5, maxFreqSet[-1][1][idxLeft])) 

	if len(not_filled_list) == 0:
		return 1

	if (letter_found == 0):
		TRIES -= 1
		displayStats()
		return -1

	return 0

def rerunGame():
	preProcessor()
	runGame()

def runGame():
	global fill_factor_list, indices_list, weighted_list, TRIES
	res_list = []
	TRIES = 3
	Automate.clearAll()
	weighted_list = [None] * len(split_input_list)

	weighted_list = map(lambda x: list(ModDict.modDict.get(str(len(x)))), split_input_list)
	Automate.calculateLetterWeightOfList(weighted_list, True)

	fill_factor_list = [0] * len(split_input_list)
	indices_list = [[]] * len(split_input_list)
	
	initializeState()
	printState()
	playGame()
	
if __name__=='__main__':

	graphviz = GraphvizOutput()
	graphviz.output_file = 'hangman_graph.png'

	with PyCallGraph(output=graphviz):
    
		print "Processing dictionary only one time..."
	
		isPassed = ModDict.loadAllDicts()
		if (not isPassed): 
			sys.exit("File not found in current directory")

		print "Finished!"
	
		preProcessor()
		runGame()
	



	
