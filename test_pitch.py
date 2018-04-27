from audio import produce_soundfile
import ast
import wave
import os

TEST_PITCH_DIR = './test_pitch/'
TEST_RATE = 720
TEST_REPEATS = 100

PITCH_MAP_STORE = './config/pitch_map.config'
def retrieve_sound_by_pitches():
    lines = [line.rstrip('\n\r') for line in open(PITCH_MAP_STORE)]
    def _parse_line(line):
        tokens = line.split(' ')
        note, sound, voice = tokens[:3]
        return (note, (sound, voice))
    return {
        note: sound_and_voice
        for note, sound_and_voice in
        [_parse_line(line) for line in lines]
    }
SOUND_BY_PITCHES = retrieve_sound_by_pitches()

REPS_PER_SECOND_STORE = './config/repeats_per_second.config'
def regenerate_reps_per_second():
    if not os.path.exists(TEST_PITCH_DIR):
        os.makedirs(TEST_PITCH_DIR)
    for note, (sound, voice) in SOUND_BY_PITCHES.iteritems():
        produce_soundfile(sound*TEST_REPEATS, voice, TEST_RATE, TEST_PITCH_DIR+note+'.wav')
    def _get_repeats_per_second(note):
        w = wave.open(TEST_PITCH_DIR+note+'.wav', mode='rb')
        time = float(w.getnframes()) / w.getframerate()
        w.close()
        return float(TEST_REPEATS) / time
    repeats_per_second = {
        note: _get_repeats_per_second(note) for note in SOUND_BY_PITCHES.iterkeys()
    }
    with open(REPS_PER_SECOND_STORE, 'w') as f:
        f.writelines([str(repeats_per_second)])

def retrieve_reps_per_second():
    def _read_from_reps_per_second_store():
        with open(REPS_PER_SECOND_STORE, 'r') as f:
            return ast.literal_eval(f.readline())
    try:
        return _read_from_reps_per_second_store()
    except SyntaxError:
        # reps_per_second.config is corrupted.  regenerate configs and try again.
        try:
            regenerate_reps_per_second()
            return _read_from_reps_per_second_store()
        except:
            print 'Failed.  Make sure pitch map and config autogeneration script are correct\
                   and try again.'
            exit()
REPS_PER_SECOND = retrieve_reps_per_second()

if __name__ == '__main__':
    regenerate_reps_per_second()
