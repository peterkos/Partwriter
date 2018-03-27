
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

	# Helper function: returns the first voice that contains the given pitch
	def findVoice(pitch, chord, index):
		voices = [bass, alto, tenor, soprano]


		for voice in voices:
			print(voice.notes[index].name)
			if (voice.notes[index].name == pitch.name):
				print("\tfound " + pitch.name + " in " + voice[0].bestName())
				return voice

		raise ValueError("Could not find a voice containing the pitch " + pitch.name + "!")


	# Loop through all chords
	for chord in chords.recurse().getElementsByClass("Chord"):
		
		chord.closedPosition(forceOctave=4, inPlace=True)

		romanNumeral = roman.romanNumeralFromChord(chord, scoreKey, True)
		chord.addLyric(str(romanNumeral.figure))

		# Check chordal seventh resolution -- 
		if (chord.isDominantSeventh()):
			
			voiceChordal7th = findVoice(chord.seventh, chord, chordIndex)

			# Check if it's not resolved correctly.
			# Chordal sevenths must resovle up by step.
			resInterval = interval.Interval(voiceChordal7th.notes[chordIndex], voiceChordal7th.notes[chordIndex + 1])
			
			if ((not resInterval.isStep) or (resInterval.direction != interval.Direction.ASCENDING)):
				resInterval.noteStart.style.color = "blue"
				print("\tChordal seventh improperly resolved at beat " + str(chordIndex + 1))
			# else:
				# resInterval.noteStart.style.color = "green"
				# print("\tChordal seventh properly resolved in " + voiceChordal7th[0].bestName() + " at beat " + str(chordIndex + 1))


		# Check scale degree 7 resolution -- 
		# TODO: Check if not raised in chord! (absolute value of note?)
		scaleSeventh = scoreKey.getLeadingTone()
		scaleSeventhInChord = [currentNote for currentNote in chord.pitches if scaleSeventh.name == currentNote.name]

		if (len(scaleSeventhInChord) == 1):

			voiceWithSeventh = findVoice(scaleSeventh, chord, chordIndex)
			resInterval = interval.Interval(voiceWithSeventh.notes[chordIndex], voiceWithSeventh.notes[chordIndex + 1])

			# If in inner voice, can leap down to scale degree 5
			if (voiceWithSeventh[0].bestName() == "Alto" or voiceWithSeventh[0].bestName() == "Tenor"):
				if (not (not resInterval.isStep and (voiceWithSeventh.notes[chordIndex + 1].name == scoreKey.pitchFromDegree(5).name))):
					resInterval.noteStart.style.color = "red"
					print("\tLeading tone improperly resolved in " + voiceChordal7th[0].bestName() + " at beat " + str(chordIndex + 1))

			# Normal resolution -- needs to resolve up by step
			if (not (resInterval.isStep and voiceWithSeventh.notes[chordIndex + 1].name == scoreKey.pitchFromDegree(1).name)):
				resInterval.noteStart.style.color = "red"
				print("\tLeading tone improperly resolved in " + voiceChordal7th[0].bestName() + " at beat " + str(chordIndex + 1))

		chordIndex += 1


	# Insert into main score
	aScore.insert(0, chords)



print()
printIntervals()
print("\n")
checkParallels()
print("\n")



voiceResolution()
# aScore.show()


