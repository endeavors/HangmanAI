import Hangman
import sys

def getAverage():

	TOTAL_TESTS = 1000000
	correct = 0
	try:
		for x in range(TOTAL_TESTS):
			tries = Hangman.main(True)
			if tries != 0:
				correct += 1
			print "\rTests Done: %d/%d" % (x+1,TOTAL_TESTS),
			sys.stdout.flush()
	except Exception,e:
		print str(e)
	
	return correct/float(TOTAL_TESTS)

if __name__ == '__main__':

	avg = getAverage()
	print "\nAverage:", "%.4f%%" % (avg*100)
		
		