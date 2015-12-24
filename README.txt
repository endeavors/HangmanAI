Run: python Hangman.py
Run and show flow graph: pycallgraph graphviz —- ./Hangman.py

How the algorithm works (Overview):
There are two things that kept track of using this algorithm: letter frequency and word frequency. If you choose to have the word generator randomly select words for the program to solve, there is no need to main word frequency list since every word has equal probability of being chosen. This is however not the case if a human decides to provide an input. You start out with list of possible words you can have for the blanks and keep finding the letter frequency of that list and then extracting the letter with the highest probability as our next guess. (A priority queue-like structure is used to order the probabilities). You keep doing this process until you have either reduced your list size to a single word, which means you’ve found the word, or there are only two letters left to be guessed for the word and the input was inputted by the human. In the latter case, you maintain word frequency of the left-over list and pick the highest probabilistic word. The algorithm is based on a probabilistic model of letter and word frequencies combined. We also keep track of fill factor that keep tracks of how filled the word in the letters we have guessed. 

You can keep playing the game as many times you wish and see in the generated flow graph the processes and time each function went through

Feel free to point out any bugs/improve it.

—-Gurkirat Singh