from sortedcontainers import SortedList
import ModDict

maxFreqSet = set()
sortedList = SortedList()

def clearAll():
	global maxFreqSet
	maxFreqSet.clear()
	sortedList.clear()

def prepForValidFoundSet(letter_set):
	
	if len(sortedList) > 0 and sortedList[-1][0] != 2:
		sortedList.clear()

	for x in letter_set:
		is_in_list = 0
		for i in reversed(sortedList):
			if i == (2,x):
				is_in_list = 1
				break
		if is_in_list == 0 and x not in maxFreqSet:		
			sortedList.add((2,x))

def evalWeight(weight_dict, ttl_chars_cnt):
	global sortedList
	sortedList.clear()
	for char,charCnt in weight_dict.iteritems():
		wratio = charCnt/float(ttl_chars_cnt)
		sortedList.add((wratio,char))

def popMaxWeightChar():

	#return just the character with the highest priority
	if (len(sortedList) > 0):
		maxWeight = sortedList.pop()

		while maxWeight[1] in maxFreqSet:
			if len(sortedList) > 0:
				maxWeight = sortedList.pop()

		maxFreqSet.add(maxWeight[1])
		return maxWeight[1]
	else:
		return None

def calculateLetterWeightOfList(weighted_List, createSet):
	
		weight_dict = {}
		ttl_chars_cnt = 0
		initSet = set() #set used for initial call to this function
		each_idx_dict = {}
		
		for idx, eachSet in enumerate(weighted_List):

			if eachSet is not None and len(eachSet) != 0:
				val_set = next(iter(eachSet))
				if createSet and len(val_set) in initSet:
					idx_dict = each_idx_dict.get(len(val_set))
					weight_dict = {val: weight_dict.get(val,0) + idx_dict.get(val,0)\
						for val in set(weight_dict) | set(idx_dict)}
				else:
					temp_dict = {} #dict specific to set
					if (createSet):
						initSet.add(len(val_set))

					for val in eachSet:
						for letter in val:
							if letter not in maxFreqSet:
								if letter in temp_dict:
									charCnt = temp_dict.get(letter) 
									charCnt += 1
									temp_dict[letter] = charCnt
								else:
									temp_dict[letter] = 1
								ttl_chars_cnt += 1

					each_idx_dict[len(val_set)]= temp_dict
					weight_dict = {val: weight_dict.get(val,0) + temp_dict.get(val,0)\
						for val in set(weight_dict) | set(temp_dict)}

		evalWeight(weight_dict,ttl_chars_cnt)

def createWordFreqSortedList(set_iterable):

	freqSortedList = SortedList()
	for word in set_iterable:
		freq = ModDict.freqDict.get(word)
		if freq != None:
			freqSortedList.add((int(freq),word))
		else:
			freqSortedList.add((0,word))

	return freqSortedList
	