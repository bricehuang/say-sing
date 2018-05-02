import sys
from test_pitch import SOUND_BY_PITCHES, REPS_PER_SECOND

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
