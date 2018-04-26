import ast
import subprocess
import sys
import time
import wave
from audio import produce_soundfile

SOUND_BY_PITCHES = {
	'F2': ('la', 'Juan'),
	'F#2': ('wa', 'Xander'),
	'G2': ('vo', 'Maged'),
	'Ab2': ('de', 'Xander'),
	'A2': ('wo', 'Yuri'),
	'Bb2': ('na', 'Yuri'),
	'B2': ('ni', 'Diego'),
	'C3': ('ra', 'Diego'),
	'C#3': ('bo', 'Luca'),
	'D3': ('mu', 'Paulina'),
	'Eb3': ('je', 'Satu'),
	'E3': ('ne', 'Satu'),
	'F3': ('le', 'Laura'), # ?
	'F#3': ('li', 'Ellen'),
	'G3': ('li', 'Alice'),
	'Ab3': ('ni', 'Damayanti'),
	'A3': ('wu', 'Luciana'),
	'Bb3': ('gi', 'Sara'),
	'B3': ('wi', 'Veena'),
	'C4': ('mi', 'Luciana'), # flat
	'C#4': ('no', 'Yuna'),
	'D4': ('li', 'Yuna'), # flat
	'Eb4': ('nu', 'Melina'),
	'E4': ('te', 'Yuna'), # derp
	'F4': ('pi', 'Yuna'),
}
REPS_PER_SECOND = {}
REPS_PER_SECOND_STORE = './repeats_per_second.txt'
if __name__ == '__main__':
	with open(REPS_PER_SECOND_STORE, 'r') as f:
		REPS_PER_SECOND = ast.literal_eval(f.readline())
IN_FILE = './in.txt'
OUT_FILE = './out.txt'

def get_command_for_note(note, length_secs):
	if note == 'res':
		return 'sleep %s ' % (length_secs)
	sound, voice = SOUND_BY_PITCHES[note]
	reps = int(round(REPS_PER_SECOND[note] * length_secs))
	return 'say %s --voice=%s --rate=720 ' % (sound*reps, voice)

SECS_PER_MIN = 60.
def get_commands_for_song(notes_and_lengths, bpm):
	return [
		get_command_for_note(note, SECS_PER_MIN * length / bpm)
		for note, length in notes_and_lengths
	]

def concat_commands(commands):
	ans = commands[0]
	for command in commands[1:]:
		ans += "&& " + command
	return ans

def parse_input(filename):
	lines = [line.rstrip('\n\r') for line in open(filename)]
	def _parse_tempo(line):
		return float(line)
	def _parse_line(line):
		note, length = line.split(' ')
		return (note, float(length))
	tempo = _parse_tempo(lines.pop(0))
	return ([_parse_line(line) for line in lines], tempo)

if __name__ == '__main__':
	in_filename = IN_FILE
	out_filename = OUT_FILE
	if len(sys.argv)>1:
		in_filename = sys.argv[1]
	if len(sys.argv)>2:
		out_filename = sys.argv[2]
	song, tempo = parse_input(in_filename)
	command = concat_commands(get_commands_for_song(song, tempo))
	with open(out_filename, 'w') as f:
		f.writelines(command)
