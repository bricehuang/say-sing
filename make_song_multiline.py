import sys
from regenerate_configs import DELAY_BY_PITCH, SOUND_BY_PITCHES, REPS_PER_SECOND

IN_FILE = './in.txt'
OUT_FILE = './out.txt'

SHIFT_DOWN = {
    'F#2': 'F2',
    'G2': 'F#2',
    'Ab2': 'G2',
    'A2': 'Ab2',
    'Bb2': 'A2',
    'B2': 'Bb2',
    'C3': 'B2',
    'C#3': 'C3',
    'D3': 'C#3',
    'Eb3': 'D3',
    'E3': 'Eb3',
    'F3': 'E3',
    'F#3': 'F3',
    'G3': 'F#3',
    'Ab3': 'G3',
    'A3': 'Ab3',
    'Bb3': 'A3',
    'B3': 'Bb3',
    'C4': 'B3',
    'C#4': 'C4',
    'D4': 'C#4',
    'Eb4': 'D4',
    'E4': 'Eb4',
    'F4': 'E4',
    'F#4': 'F4',
    'res': 'res',
}

def compile_note(note, length_secs):
    if note == 'res':
        return 'sleep %s ' % (length_secs)
    sound, voice = SOUND_BY_PITCHES[note]
    reps = int(round(REPS_PER_SECOND[note] * length_secs))
    return 'say %s --voice=%s --rate=720 ' % (sound*reps, voice)

def compile_line(line, bpm, delay):
    delay_cmd = ['sleep %s' % (delay)] if delay > 0 else []
    return '( ' + ' && '.join(delay_cmd + [compile_note(SHIFT_DOWN[note], SECS_PER_MIN*length / bpm) for note, length in line]) + ' )'

def compile_sync_unit(sync_unit, bpm):
    wait_cmd = ['wait'] if len(sync_unit) > 1 else []
    nlines = len(sync_unit)
    delays = [(DELAY_BY_PITCH[SHIFT_DOWN[line[0][0]]] if line[0][0] != 'res' else 0 ) for line in sync_unit ]
    max_delay = max(delays)
    return '( ' + ' & '.join([compile_line(sync_unit[i], bpm, max_delay - delays[i]) for i in range(nlines)] + wait_cmd) + ' )'

def compile_song(song, bpm):
    return ' &&\n'.join(compile_sync_unit(sync_unit, bpm) for sync_unit in song)

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
    return ans + "\n"

def parse_into_sync_units(lines):
    sync_units = []
    def _parse_line(line):
        tokens = line.split(' ')
        assert len(tokens)%2 == 0, line
        parsed = []
        while tokens:
            note, length = tokens[:2]
            tokens = tokens[2:]
            parsed.append((note, float(length)))
        return parsed

    for line in lines:
        if line == '-----':
            sync_units.append([])
        else:
            sync_units[-1].append(_parse_line(line))
    return sync_units

def parse_input(filename):
    lines = [line.rstrip('\n\r') for line in open(filename)]
    def _parse_line(line):
        note, length = line.split(' ')
        return (note, float(length))
    tempo = float(lines.pop(0))
    return (parse_into_sync_units(lines), tempo)
    # return ([_parse_line(line) for line in lines], tempo)

if __name__ == '__main__':
    in_filename = sys.argv[1] if len(sys.argv)>1 else IN_FILE
    out_filename = sys.argv[2] if len(sys.argv)>2 else OUT_FILE
    song, tempo = parse_input(in_filename)
    command = compile_song(song, tempo)
    with open(out_filename, 'w') as f:
        f.writelines(command)
