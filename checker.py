
from music21 import *

# NOTE: 
#	Will be condensed into a class eventually. 
# 	I just don't want to type "self. self. self. self." before every part!



# class ScoreParse:

# 	def __init__(self, name):
# 		self.theScore   = converter.parse(name)
# 		# sBach = corpus.parse("bach/bwv57.8.xml")
# 		self.soprano = self.score.parts[0]
# 		self.alto    = self.score.parts[1]
# 		self.tenor   = self.score.parts[2]
# 		self.bass    = self.score.parts[3]


aScore = converter.parse("testscore.xml")

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


def voiceResolution():
	chords = aScore.chordify()
	scoreKey = aScore.analyze("key")

	# chordIndex allows us to index the current node in a given voice, so
	# we can compare the ith+1 note and check resolutions.
	chordIndex = 0

	# Loop through all chords
	for chord in chords.recurse().getElementsByClass("Chord"):
		
		print(chord)
		chord.closedPosition(forceOctave=4, inPlace=True)
		print(chord)

		romanNumeral = roman.romanNumeralFromChord(chord, scoreKey, True)
		chord.addLyric(str(romanNumeral.figure))

		# Check chordal seventh resolution -- 
		if (chord.isDominantSeventh()):
				
			# Find which voice has the seventh
			voiceWithChordalSeventh = findVoice(7, chord, chordIndex)

			# Check if it's not resolved correctly.
			# Chordal sevenths must resovle up by step.
			resInterval = interval.Interval(voiceWithChordalSeventh.notes[chordIndex], voiceWithChordalSeventh.notes[chordIndex + 1])
			
			if ((not resInterval.isStep) or (resInterval.direction != interval.Direction.ASCENDING)):
				
				# Change color
				resInterval.noteStart.style.color = "blue"
				print("\tImproperly resolved at beat " + str(chordIndex + 1))
			else:
				print("\tChord properly resolved in " + voiceWithChordalSeventh[0].bestName() + " at beat " + str(chordIndex))



		# Check scale degree 7 resolution -- 
		# Precondition: Dominant (V) chord only!

		voiceWithSeventh = findVoice(3, chord, chordIndex)
		scaleSeventh = scoreKey.pitches[7 - 1].name

		if (scaleSeventh.accidental is None):
			raise ValueError("Scale Degree 7th is not raised at beat" + str(chordIndex))

		
		# TODO: Fix findVoice method to be relative to scale, not relative to chord!

	
		# If in inner voice, can leap down to scale degree 5
		# if (voiceWithSeventh == alto or voiceWithSeventh == tenor):

		
		


		chordIndex += 1


	# Insert into main score
	aScore.insert(0, chords)
	# aScore.show()


# Returns the voice that contains the given degree
def findVoice(degreeNumber, chord, index):
	voiceWithDegree = -1
	voices = [bass, alto, tenor, soprano]

	for voice in voices:
		if (voice.notes[index].name == chord.getChordStep(degreeNumber).name):
			voiceWithDegree = voice
			print("found in " + voice[0].bestName())

	# TODO: Add chord/measure number
	if (voiceWithDegree == -1):
		raise ValueError("Could not find a voice containin the seventh!")

	return voiceWithDegree





print()
printIntervals()
print("\n")
checkParallels()
print("\n")



voiceResolution()
aScore.show()


