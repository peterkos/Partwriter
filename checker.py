
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
	

	def compareVoice(v1, v2):

		for i in range(0, len(intervals[soprano]) - 1):

			# print("Sop at " + str(i) + ": " + str(intervals[soprano][i].noteStart))
			# print("Alt at " + str(i) + ": " + str(intervals[alto][i].noteStart))

			intervalBetween = interval.Interval(intervals[v1][i].noteStart, intervals[v2][i].noteStart)

			if ((intervals[v1][i].simpleName == intervals[v2][i].simpleName) and \
				(intervalBetween.simpleName == "P5" or intervalBetween == "P8")):
				
				# TODO: Cleanup, and add measure location! Goal: color notes!
				print("Parallel " + intervalBetween.simpleName + \
					  " between " + str(v1[0].bestName()) + " and " + str(v2[0].bestName()) + \
					  " across beats " + str(i + 1) + " and " + str(i + 2))

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

# soprano.show()
# aScore.show()

