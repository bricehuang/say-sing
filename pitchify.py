import ast
import math
from audio_master import OUT_DIR, VOICES

PITCHES = [440 * (2**(1./12))**i for i in xrange(-28, 4)] # F2 - C5
TOLERANCE = 2**(20./1200) # 20 cents
PITCH_NAMES = [
	'F2','F#2','G2','Ab2','A2','Bb2','B2',
	'C3','C#3','D3','Eb3','E3','F3','F#3','G3','Ab3','A3','Bb3','B3',
	'C4','C#4','D4','Eb4','E4','F4','F#4','G4','Ab4','A4','Bb4','B4',
	'C5',
]

def parse_voice(voice):
	# type: (str) -> List[Tuple[float, float, Tuple[str, str]]]
	with open(OUT_DIR + voice + '.out') as f:
		return ast.literal_eval(f.readline())

def construct_master():
	# type: () -> List[Tuple[float, float, Tuple[str, str]]]
	master_good_sounds = []
	for voice in VOICES:
		master_good_sounds += parse_voice(voice)
	return master_good_sounds

def get_matching_sounds(pitch, good_sounds):
	# type: (float, List[Tuple[float, float, Tuple[str, str]]]) -> List[Tuple[float, float, Tuple[str, str]]]
	low = pitch / TOLERANCE
	high = pitch * TOLERANCE
	result = []
	for pitch, sqamp, sound_and_voice in good_sounds:
		if (pitch >= low and pitch <= high):
			result.append((pitch, sqamp, sound_and_voice))
	result.sort(key = lambda (pitch, sqamp, sound_and_voice): sqamp, reverse=True)
	return result

def format_as_diff_from_pitch(base_pitch, sound):
	# type: (float, List[Tuple[float, float, Tuple[str, str]]]) -> List[Tuple[float, float, Tuple[str, str]]]
	def _diff_from_pitch_in_cents(base_pitch, pitch):
		return 1200.*math.log(pitch/base_pitch)/math.log(2)
	pitch, sqamp, sound_and_voice = sound
	return (_diff_from_pitch_in_cents(pitch, base_pitch), sqamp, sound_and_voice)

if __name__ == '__main__':
	master_good_sounds = construct_master()
	with open(OUT_DIR+'master.out', 'w') as f:
		f.writelines(str(master_good_sounds))

	# print master_pitches_and_sounds
	output = []
	for pitch, pitch_name in zip(PITCHES, PITCH_NAMES):
		output.append(pitch_name+': ' + str(pitch) + '\n')
		matching_sounds = get_matching_sounds(pitch, master_good_sounds)
		for matching_sound in matching_sounds:
			output.append(str(format_as_diff_from_pitch(pitch, matching_sound))+'\n')
		output.append('\n')
	with open('pitches.out', 'w') as f:
		f.writelines(output)
