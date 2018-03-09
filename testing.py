
# from abjad import *
# import mido
from music21 import *



# # notes = [Note("c'4"), Note("a'4"), Note("c'4")]
# notes = []

# for i in range(0, 10):
# 	notes.append(Note(i, Duration(1, 4)))

# show(Container(notes))




# mid = mido.MidiFile("miditest.mid")
# for message in mid.play():
# 	print(message.type)


# THIS IS LITERALLY MAGIC
# score = corpus.parse("bach/bwv65.2.xml")
# print(score.analyze("key"))
# score.show()


note1 = note.Note("C4")
note2 = note.Note("F#4")

note1.duration.type = "half"
note1.duration.quarterLength
note2.duration.quarterLength

notes = [note1, note2]

# for thisNote in notes:
	# print(thisNote.step)


stream1 = stream.Stream()

stream1.append(note1)
stream1.append(note2)

stream2 = stream.Stream()
note3 = note.Note("D#5")
stream2.repeatAppend(note3, 4) # appends 4 of note 3 to stream2
# stream2.show("text")
# stream2.show()


# for thisNote in stream1.notes:
	# print(thisNote.step)


### CHORDS


cMinor = chord.Chord(["C4", "G4", "E-5"])
cMinor.duration.type = "half"
# for currentPitch in cMinor.pitches:
	# print(currentPitch)


# Tuples
#	Indexable, but immutable.
#	.pitches() returns a tuple

# if cMinor.isMajorTriad():
	# print("cMinor is major in " + str(cMinor.inversion()) + " inversion")
# else:
	# print("cMinor is minor in " + str(cMinor.inversion()) + " inversion")

# cMinor.closedPosition().show()

