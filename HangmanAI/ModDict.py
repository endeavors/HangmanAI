import json, io
import os.path
import pprint

modDict = {}
freqDict = {}

def createModDict():
	with open('dict.txt','r') as data_file:
		for word in data_file:
			word = word.strip().lower()
			if len(word) in modDict:
				wordsOfSpecificLength = modDict[len(word)]
				wordsOfSpecificLength.append(word)
				modDict[len(word)] = wordsOfSpecificLength
			else:
				wordsOfSpecificLength = [word]
				modDict[len(word)] = wordsOfSpecificLength

	with open ('ModDict.json', 'w') as outfile:
		json.dump(modDict, outfile, sort_keys=True, indent = 4, ensure_ascii=False)

def loadAllDicts():

	global modDict, freqDict

	modDictFile = "./ModDict.json"
	freqDictFile = "./FreqDict.json"

	if not os.path.isfile(modDictFile):
		try:
			createModDict()
		except:
			return False

	with open(modDictFile,'r') as data_file:
		modDict = json.load(data_file)
			
	if not os.path.isfile(freqDictFile):
		try:
			parseFreqDict()
		except:
			return False

	with open(freqDictFile,'r') as data_file:
		freqDict = json.load(data_file)
			
	return True

def parseFreqDict():
	
	with open('freq.txt','r') as data_file:
		for line in data_file:
			freqLine = map(lambda x: x.strip(),line.lower().split())
			freqDict[freqLine[0]] = freqLine[1]
			
	with open ('FreqDict.json', 'w') as outfile:
		json.dump(freqDict, outfile, sort_keys=True, indent = 4, ensure_ascii=False)
