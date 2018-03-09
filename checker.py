
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

	# Streams for intervals
	intervals = {}
	intervals[soprano] = soprano.notes.melodicIntervals()
	intervals[alto] = alto.notes.melodicIntervals()
	intervals[tenor] = tenor.notes.melodicIntervals()
	intervals[bass] = bass.notes.melodicIntervals()

	# Actually compare
	for i in range(0, len(intervals[soprano]) - 1):

		# print(intervals[soprano].name, intervals[alto].name, intervals[tenor].name, intervals[bass].name)

		def compareVoice(v1, v2):
			if (intervals[v1][i].name == intervals[v1][i].name and intervals[v1][i + 1].name == intervals[v1][i + 1].name):
				print("Parallel " + intervals[v1][i].niceName + "s" + " between " + str(v1[0]) + " and " + str(v2[1]))

		compareVoice(bass, tenor)
		compareVoice(bass, alto)
		compareVoice(bass, soprano)
		compareVoice(tenor, alto)
		compareVoice(tenor, soprano)
		compareVoice(alto, soprano)


printIntervals()
print()
checkParallels()

# soprano.show()
# aScore.show()

