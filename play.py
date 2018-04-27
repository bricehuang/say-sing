import ast
import subprocess
import sys
import time
import wave
from audio import produce_soundfile

PITCH_MAP = './config/pitch_map.config'
def retrieve_sound_by_pitches():
    lines = [line.rstrip('\n\r') for line in open(PITCH_MAP)]
    def _parse_line(line):
        note, sound, voice = line.split(' ')
        return (note, (sound, voice))
    return {
        note: sound_and_voice
        for note, sound_and_voice in
        [_parse_line(line) for line in lines]
    }
SOUND_BY_PITCHES = retrieve_sound_by_pitches()

REPS_PER_SECOND = {}
REPS_PER_SECOND_STORE = './config/repeats_per_second.config'
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
        ans += "&&\n" + command
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
    in_filename = sys.argv[1] if len(sys.argv)>1 else IN_FILE
    out_filename = sys.argv[2] if len(sys.argv)>2 else OUT_FILE
    song, tempo = parse_input(in_filename)
    command = concat_commands(get_commands_for_song(song, tempo))
    with open(out_filename, 'w') as f:
        f.writelines(command)
