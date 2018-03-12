
from music21 import *

# class ScoreParse:

# 	def __init__(self, name):
# 		self.theScore   = converter.parse(name)
# 		# sBach = corpus.parse("bach/bwv57.8.xml")
# 		self.soprano = self.score.parts[0]
# 		self.alto    = self.score.parts[1]
# 		self.tenor   = self.score.parts[2]
# 		self.bass    = self.score.parts[3]


aScore = converter.parse("asdf.xml")

soprano  = aScore.parts[0].flat
alto     = aScore.parts[1].flat
tenor    = aScore.parts[2].flat
bass     = aScore.parts[3].flat



def printIntervals():
	print("Soprano:  ", end="")
	for interval in soprano.notes.melodicIntervals():
		print(interval.name, end=" ")

	print()
	print("Alto:     ", end="")
	for interval in alto.notes.melodicIntervals(): 
		print(interval.name, end=" ")

	print()
	print("Tenor:    ", end="")
	for interval in tenor.notes.melodicIntervals(): 
		print(interval.name, end=" ")

	print()
	print("Bass:     ", end="")
	for interval in bass.notes.melodicIntervals(): 
		print(interval.name, end=" ")


def checkParallels(): 

	# Colors to distinguish simultaenous parallels
	# TODO: Garuntee different colors? Different colors for P5 and P8?
	import itertools
	colors = ["blue", "green", "red", "cyan", "magenta"]
	colorGen = itertools.cycle(colors)

	# Function to compare
	def compareVoice(v1, v2):

		for i in range(len(v1.notes) - 1):

			firstInterval = interval.Interval(v1.notes[i], v2.notes[i])
			secondInterval = interval.Interval(v1.notes[i + 1], v2.notes[i + 1])

			if (firstInterval.simpleName == secondInterval.simpleName and \
				firstInterval.simpleName == "P5" or firstInterval.simpleName == "P8"):
				
				print("Parallel " + firstInterval.simpleName + \
					  " between " + str(v1[0].bestName()) + " and " + str(v2[0].bestName()) + \
					  " across beats " + str(i + 1) + " and " + str(i + 2))

				# Change color of affected notes
				currentColor = next(colorGen)
				v1.notes[i].style.color     = currentColor
				v1.notes[i + 1].style.color = currentColor
				v2.notes[i].style.color     = currentColor
				v2.notes[i + 1].style.color = currentColor


	# Compare each voice respectively, bottom-up 
	compareVoice(bass, tenor)
	compareVoice(bass, alto)
	compareVoice(bass, soprano)
	compareVoice(tenor, alto)
	compareVoice(tenor, soprano)
	compareVoice(alto, soprano)


print()
printIntervals()
print("\n")
checkParallels()
print("\n")


aScore.show()
