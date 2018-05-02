# Say Command Song Generator

This app sings songs using only the `say` command from Mac Terminal, leveraging the fact that `say`, run on a short, repeated syllable spoken very quickly, can approximate a pitch.  For example,
```
say wuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwu --voice=Luciana --rate=720
```
approximates the pitch A3.  By varying the syllable and voice, it is possible to get a wide range of pitches.

Given a melody, this app composes a combination of `say` commands that sings this melody.  Example outputs can be found in `sample_out/`.

## Getting Started

This app should work out of the box, on a computer with Mac Terminal and Python 2.7 installed.

## Usage

The main usage is
```
python play.py [in_file] [out_file]
```
This writes to `out_file` a `say` command that sings the melody from `in_file`.  Default in and out files are `in.txt` and `out.txt`.
For example:
```
python play.py sample_in/birthday2.txt sample_out/birthday2.txt
eval $(cat sample_out/birthday2.txt)
```
writes a `say` command sequence for Happy Birthday to `sample_out/birthday2.txt` and executes these commands.

The first line in each input file is the tempo in BPM, and each subsequent line is a note and duration in beats.  Currently supported notes are F2-F4.  See `sample_in/` for examples of input formatting.

### Changing the Pitch Map

The map from pitch to `(syllable, voice)` is stored in `config/pitch_map.config`.  Candidate `(syllable, voice)` combinations for each pitch are stored in `pitches.out`, in the format
```
(pitch_diff, purity, (syllable, voice))
```
where `pitch_diff` is the difference from the true note in cents, and `purity` is a 0-1 score of how clean the pitch is.

After changing the pitch map, run
```
python test_pitch.py
```
to regenerate auto-generated configs before running `play.py`.

### Methodology for Generating Pitch Data

For each `(syllable, voice)` combination, I extract a waveform from the `say` soundfile and Fourier transform it, then extract the largest frequencies.  The data-analysis scripts are as follows:
* `audio.py`: processes all `(syllable, voice)` combinations for a given voice, and prints `(syllable, voice, frequency, goodness)` results to `outfiles/[voice].out`.  Usage: `python audio.py [voice]`.
* `pitchify.py`: consolidates the outfiles from `audio.py`.  Finds candidate `(syllable, voice)` combinations for each pitch and prints them to `pitches.out`.
* `audio_master.py`: dispatches `audio.py` for each voice, then dispatches `pitchify.py`.
* `audio_test.py`: util script that plays a `say` command with given syllable and voice.  Usage: `python audio.py [syllable] [voice]`.

## License

This project is licensed under the MIT License.

## Acknowledgments

Thanks to Next 4W and the MIT Undergrad Math Lounge for putting up with my obnoxious sound experimentation :)
