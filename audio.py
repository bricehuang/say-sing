import numpy as np
import struct
import subprocess
import sys
import wave

CONSONANTS = ['', 'p', 'b', 't', 'd', 'k', 'g', 'm', 'n', 'r', 'f', 'v', 'th', 'j', 's', 'z', 'sh', 'zh', 'h', 'l', 'w', 'y']
VOWELS = ['a', 'e', 'i', 'o', 'u']
REPEATS = 100
RATE = 720
SOUNDFILE = 'out.wav'
PRE_CONSOLIDATION_SIGNIFICANCE_CUTOFF = 1e-3
POST_CONSOLIDATION_SIGNIFICANCE_CUTOFF = 1e-2
POST_OVERTONE_CONSOLIDATION_SIGNIFICANCE_CUTOFF = 1e-1
PITCH_SIMILARITY_RATIO_CUTOFF = 1e-2
OVERTONE_ROUNDING_ERROR_CUTOFF = 1e-2
OVERTONE_SQAMP_RATIO_CUTOFF = 0.5
OUT_DIR = './outfiles/'
def produce_soundfile(word, voice, rate, filename=SOUNDFILE):
	# type: (str, str, int) -> None
	"""
		Outputs soundfile of voice saying word at rate to file named filename
	"""
	subprocess.call(
		['say', word, '-v', voice, '-r', str(rate), '-o', filename, '--data-format=LEI32@22050']
	)

def parse_wav_file(filename=SOUNDFILE):
	# type: (str) -> {data: List[int], framerate: int}
	"""
		Parses a sound file into a waveform (int array) and framerate.
	"""
	w = wave.open(filename, mode='rb')
	data = [struct.unpack('<i',w.readframes(1))[0] for i in xrange(w.getnframes())]
	w.close()
	return {
		'data': data,
		'framerate': w.getframerate(),
	}

def normalize(amps):
	# type: (List[float]) -> List[float]
	"""
		Normalizes a frequency/square-amplitude vector to norm 1.
	"""
	mag = sum(amps)
	return [amp/mag for amp in amps]

def normalized_freq_amps(signal):
	# type: {data: List[int], framerate: int} -> {amps: List[float], freq_scale: float}
	"""
		Extracts a normalized frequency/square-amplitude vector.  freq_scale means that amps[i]
		represents the square-amplitude of frequenecy freq_scale * i.  The zero-frequency term,
		which carries no information about the wave, is forced to 0.
	"""
	data = signal['data']
	unnormalized_amps = [abs(entry)**2 for entry in np.fft.rfft(data)]
	unnormalized_amps[0] = 0
	return {
		'amps': normalize(unnormalized_amps),
		'freq_scale': float(signal['framerate'])/len(data)
	}

def get_significant_freqs(freq_signal):
	# type: ({amps: List[float], freq_scale: float}) -> List[Tuple[float, float]]
	"""

	"""
	amps = freq_signal['amps']
	significant_freqs = [
		(freq_signal['freq_scale'] * i, amps[i])
		for i in xrange(len(amps))
		if amps[i] > PRE_CONSOLIDATION_SIGNIFICANCE_CUTOFF
	]
	return significant_freqs

def consolidate_significant_freqs(freqs_and_amps):
	# type: List[Tuple[float, float]] -> List[Tuple[float, float]]
	"""
		Consolidates (freq, sqamp) whose frequencies are within a factor of
		1+-PITCH_SIMILARITY_RATIO_CUTOFF of each other.
		Returns consolidated list in increasing frequency order.
	"""
	def _is_pitch_similar(base, other):
		ratio = other / base
		return (
			ratio > 1 - PITCH_SIMILARITY_RATIO_CUTOFF and
			ratio < 1 + PITCH_SIMILARITY_RATIO_CUTOFF
		)
	working_freqs = list(freqs_and_amps)
	working_freqs.sort(key = lambda (freq, amp): amp, reverse = True)
	def _extract_next_freq():
		# () -> Tuple[float, float]
		"""
			Returns a consolidated (pitch, square amplitude) representing the biggest-amplitude
			pitch left in working_freqs and all pitches similar to it.  Deletes these frequencies
			from working_freqs.
		"""
		base_pitch, _ = working_freqs[0]
		pitches_to_consolidate = []
		for elt in working_freqs:
			if _is_pitch_similar(base_pitch, elt[0]):
				pitches_to_consolidate.append(elt)
		for elt in pitches_to_consolidate:
			working_freqs.remove(elt)
		total_sqamp = sum(sqamp for _, sqamp in pitches_to_consolidate)
		averaged_freq = sum(freq * sqamp for freq, sqamp in pitches_to_consolidate) / total_sqamp
		return (averaged_freq, total_sqamp)

	consolidated_freqs = []
	while len(working_freqs) > 0:
		freq, sqamp = _extract_next_freq()
		if sqamp > POST_CONSOLIDATION_SIGNIFICANCE_CUTOFF:
			consolidated_freqs.append((freq, sqamp))
	consolidated_freqs.sort(key = lambda (freq, amp): freq)
	return consolidated_freqs

def consolidate_with_overtones(freqs_and_amps):
	# type: List[Tuple[float, float]] -> List[Tuple[float, float]]
	def _is_overtone(base_freq_and_amp, other_freq_and_amp):
		base_freq, base_amp = base_freq_and_amp
		other_freq, other_amp = other_freq_and_amp
		ratio = other_freq/base_freq
		error = ratio - round(ratio)
		return (
			round(ratio) > 1.9 and
			error < OVERTONE_ROUNDING_ERROR_CUTOFF and error > - OVERTONE_ROUNDING_ERROR_CUTOFF and
			other_amp / base_amp < OVERTONE_SQAMP_RATIO_CUTOFF
		)
	working_freqs = list(freqs_and_amps)
	freqs_and_amps_with_overtones = []
	while len(working_freqs) > 0:
		base_freq, base_amp = working_freqs.pop(0)
		overtone_amp_sum = sum(
			other_amp for other_freq, other_amp in working_freqs
			if _is_overtone((base_freq, base_amp), (other_freq, other_amp))
		)
		if base_amp + overtone_amp_sum > POST_OVERTONE_CONSOLIDATION_SIGNIFICANCE_CUTOFF:
			freqs_and_amps_with_overtones.append((base_freq, base_amp + overtone_amp_sum))
	return freqs_and_amps_with_overtones

def compute_main_frequencies(sound, repeats, voice, rate):
	# type: (str, int, str, int) -> List[Tuple[float, float]]
	produce_soundfile(sound * repeats, voice, 720)
	freq_signal = normalized_freq_amps(parse_wav_file())
	significant_freqs = get_significant_freqs(freq_signal)
	consolidated_freqs = consolidate_significant_freqs(significant_freqs)
	including_overtones = consolidate_with_overtones(consolidated_freqs)
	return including_overtones

def run_all_sounds(voice):
	# type: (str) -> List[Tuple[float, float, Tuple[str, str]]]
	good_sounds = []
	for vowel in VOWELS:
		for consonant in CONSONANTS:
			sound = consonant + vowel
			try:
				frequencies_and_sqamps = compute_main_frequencies(sound, REPEATS, voice, RATE)
			except:
				print ('failed: ' + voice + ' ' + sound)
			else:
				for frequency, sqamp in frequencies_and_sqamps:
					good_sounds.append((frequency, sqamp, (sound, voice)))
	return good_sounds

if __name__ == '__main__':
	voice = sys.argv[1]
	good_sounds = run_all_sounds(voice)
	with open(OUT_DIR + voice + '.out', 'w') as f:
		f.writelines([str(good_sounds)])

