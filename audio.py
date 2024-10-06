import subprocess
import os
from rich.progress import track
from pydub import AudioSegment
from basis import NoteType

def toWav(m):
	print('Convent Into Wav Format')
	subprocess.run(
		[
			'ffmpeg',
			'-i',
			f'{m}',
			'-vn',
			'-ar',
			'44100',
			'-f',
			'wav',
			f'{m}.wav'
		]
	)
	os.remove(m)
	return f'{m}.wav'
	
def processSoundEffect(m, chart):
	tap = AudioSegment.from_file('Assests/tap.wav') + 5
	flick = AudioSegment.from_file('Assests/flick.wav') + 5
	drag = AudioSegment.from_file('Assests/drag.wav') + 5
	
	name = m
	m = AudioSegment.from_file(m)
	
	t = []
	for line in track(chart.lines, description = 'Count Notes'):
		for note in line.notes:
			t.append(
				(
					note.seconds,
					note.type
				)
			)
	
	for p in track(t, description = 'Apply Sound Effect'):
		time = round(p[0] * 1000)
		match p[1]:
			case NoteType.TAP:
				m = m.overlay(tap, position = time)
			case NoteType.HOLD:
				m = m.overlay(tap, position = time)
			case NoteType.FLICK:
				m = m.overlay(flick, position = time)
			case NoteType.DRAG:
				m = m.overlay(drag, position = time)
	m.export(name, format="wav")