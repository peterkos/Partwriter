
from music21 import *



"""
	This class provides basic analysis methods relating to partwriting practices.
	
	It currently outputs any errors to the console, and colors the specific notes that are wrong,
	according to the following:
		Blue: Parallels
		Red: Incorrect resolution of leading tone

"""
class ScoreParse:

	def __init__(self, name):
		self.localScore = converter.parse(name)
		self.soprano    = self.localScore.parts[0].flat
		self.alto       = self.localScore.parts[1].flat
		self.tenor      = self.localScore.parts[2].flat
		self.bass       = self.localScore.parts[3].flat

		self.chords 	= self.localScore.chordify()
		self.scoreKey 	= self.localScore.analyze("key")

	def printIntervals(self):
		print("Soprano:  ", end="")
		for interval in self.soprano.notes.melodicIntervals():
			print(interval.name, end=" ")

		print()
		print("Alto:     ", end="")
		for interval in self.alto.notes.melodicIntervals(): 
			print(interval.name, end=" ")

		print()
		print("Tenor:    ", end="")
		for interval in self.tenor.notes.melodicIntervals(): 
			print(interval.name, end=" ")

		print()
		print("Bass:     ", end="")
		for interval in self.bass.notes.melodicIntervals(): 
			print(interval.name, end=" ")


	def checkParallels(self): 

		# Function to find parallels between two given voices
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
					v1.notes[i].style.color     = "blue"
					v1.notes[i + 1].style.color = "blue"
					v2.notes[i].style.color     = "blue"
					v2.notes[i + 1].style.color = "blue"


		# Compare each voice respectively, bottom-up 
		compareVoice(self.bass,  self.tenor)
		compareVoice(self.bass,  self.alto)
		compareVoice(self.bass,  self.soprano)
		compareVoice(self.tenor, self.alto)
		compareVoice(self.tenor, self.soprano)
		compareVoice(self.alto,  self.soprano)


	def voiceResolution(self):
		self.chords = self.localScore.chordify()
		self.scoreKey = self.localScore.analyze("key")

		# chordIndex allows us to index the current node in a given voice, so
		# we can compare the ith+1 note and check resolutions.
		chordIndex = 0

		# Helper function: returns the first voice that contains the given pitch
		def findVoice(pitch, chord, index):
			voices = [self.bass, self.alto, self.tenor, self.soprano]

			for voice in voices:
				print(voice.notes[index].name)
				if (voice.notes[index].name == pitch.name):
					print("\tfound " + pitch.name + " in " + voice[0].bestName())
					return voice

			raise ValueError("Could not find a voice containing the pitch " + pitch.name + "!")


		# Loop through all chords
		for chord in self.chords.recurse().getElementsByClass("Chord"):
			
			chord.closedPosition(forceOctave=4, inPlace=True)

			# Check chordal seventh resolution -- 
			if (chord.isDominantSeventh()):
				
				voiceChordal7th = findVoice(chord.seventh, chord, chordIndex)

				# Check if it's not resolved correctly.
				# Chordal sevenths must resovle up by step.
				resInterval = interval.Interval(voiceChordal7th.notes[chordIndex], voiceChordal7th.notes[chordIndex + 1])
				
				if (not (resInterval.isStep or (resInterval.direction == interval.Direction.ASCENDING))):
					resInterval.noteStart.style.color = "red"
					print("\tChordal seventh improperly resolved at beat " + str(chordIndex + 1))


			# Check scale degree 7 resolution -- 
			# TODO: Check if not raised in chord! (absolute value of note?)
			scaleSeventh = self.scoreKey.getLeadingTone()
			scaleSeventhInChord = [currentNote for currentNote in chord.pitches if scaleSeventh.name == currentNote.name]

			if (len(scaleSeventhInChord) == 1):

				voiceWithSeventh = findVoice(scaleSeventh, chord, chordIndex)
				resInterval = interval.Interval(voiceWithSeventh.notes[chordIndex], voiceWithSeventh.notes[chordIndex + 1])

				# If in inner voice, can leap down to scale degree 5
				if (voiceWithSeventh[0].bestName() == "Alto" or voiceWithSeventh[0].bestName() == "Tenor"):
					if (not (not resInterval.isStep and (voiceWithSeventh.notes[chordIndex + 1].name == self.scoreKey.pitchFromDegree(5).name))):
						resInterval.noteStart.style.color = "red"
						print("\tLeading tone improperly resolved in " + voiceChordal7th[0].bestName() + " at beat " + str(chordIndex + 1))

				# Normal resolution -- needs to resolve up by step
				if (not (resInterval.isStep and voiceWithSeventh.notes[chordIndex + 1].name == self.scoreKey.pitchFromDegree(1).name)):
					resInterval.noteStart.style.color = "red"
					print("\tLeading tone improperly resolved in " + voiceChordal7th[0].bestName() + " at beat " + str(chordIndex + 1))

			chordIndex += 1


	# TODO: Which notes to color?
	def chordMembers(self):

		# chordIndex allows us to index the current node in a given voice, so
		# we can compare the ith+1 note and check resolutions.
		chordIndex = 0

		# Loop through all chords
		for chord in self.chords.recurse().getElementsByClass("Chord"):
			
			chord.closedPosition(forceOctave=4, inPlace=True)

			# Check for missing notes in chord
			if (chord.root is None):
				print("Missing root at beat " + str(chordIndex + 1))

			if (chord.third is None):
				print("Missing third at beat " + str(chordIndex + 1))

			# Check for doubled leading tone
			scaleSeventh = self.scoreKey.getLeadingTone()
			scaleSeventhInChord = [currentNote for currentNote in chord.pitches if scaleSeventh.name == currentNote.name]

			if (scaleSeventhInChord == 2):
				print("Doubled leading tone at beat " + str(chordIndex + 1))

			chordIndex += 1



	def reduceOnScore(self):
		# Loop through all chords
		for chord in self.chords.recurse().getElementsByClass("Chord"):
			chord.closedPosition(forceOctave=4, inPlace=True)
			romanNumeral = roman.romanNumeralFromChord(chord, self.scoreKey, True)
			chord.addLyric(str(romanNumeral.figure))

		self.localScore.insert(0, self.chords)


sParse = ScoreParse("testscore.xml")
print()
sParse.printIntervals()
print("\n")
sParse.checkParallels()
print("\n")
sParse.voiceResolution()
print("\n")
sParse.chordMembers()
sParse.reduceOnScore()


