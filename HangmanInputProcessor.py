from random import randint
import sys, ModDict

class HangmanInputProcessor:
    MAX_WORDS = 10 #default
    MIN_WORDS = 1
    MAX_STR_LEN = 15 #largest len found in dictionary provided

    def __init__(self,toAvg):
        self.toAvg = toAvg
        self.split_input_list = []
        self.input_choice = 0
        self.preProcessor()

    def requireInput(self):
		while (True):
			str_input = raw_input("--> Enter input: ")
			self.split_input_list = str_input.lower().split()

			if len(self.split_input_list) > HangmanInputProcessor.MAX_WORDS:
				print "Maximum string length is 10\n"
				continue

			dirty_list = filter(lambda x: self.binarySearch(x, ModDict.modDict.get(str(len(x)))) == 0,\
				self.split_input_list)

			if (dirty_list == None or len(dirty_list) != 0):
				print "The following words are not found in the dictionary:",\
					",".join(dirty_list), ". Re-enter input.\n"
			else:
				print "Entered Input:", " ".join(self.split_input_list)
				break

    def generate_input(self):
		ret_list = []
		word_num = randint(HangmanInputProcessor.MIN_WORDS,HangmanInputProcessor.MAX_WORDS)
		for rang in range(word_num):
			str_len = str(randint(HangmanInputProcessor.MIN_WORDS,HangmanInputProcessor.MAX_STR_LEN))
			while (str_len not in ModDict.modDict):
				str_len = str(randint(HangmanInputProcessor.MIN_WORDS,HangmanInputProcessor.MAX_STR_LEN))

			array = ModDict.modDict.get(str_len)
			chosen_word = array[randint(0,len(array) - 1)]
			ret_list.append(chosen_word.lower())
		return ret_list

    def preProcessor(self):
		if self.toAvg:
			self.input_choice = 1
			self.split_input_list = self.generate_input()
			return

		while (True):
			print "1 : Generate input for me"
			print "2 : Enter custom input"
			print "Type 'out' to exit program"

			try:
				self.input_choice = raw_input("--> ")

				if self.input_choice == "1":
					#list of strings
					self.split_input_list = self.generate_input()
					print "Generated Input:", " ".join(self.split_input_list)
					break

				elif self.input_choice == "2":
					self.requireInput()
					break
				elif self.input_choice == "out":
					sys.exit(0)
				else:
					print "Not a possible option\n"
			except Exception,e:
				print "Error:", str(e)

    def binarySearch(self,word,wordList):
		list_len = len(wordList)
		if (list_len == 0):
			return False

		mid = list_len/2
		chosenWord = wordList[mid].lower()
		if (chosenWord == word):
			return True
		elif chosenWord > word:
			return self.binarySearch(word,wordList[:mid])
		elif chosenWord < word:
			return self.binarySearch(word,wordList[mid+1:])
