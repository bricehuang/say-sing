# Say Command Song Generator

This app sings songs using only the `say` command from Mac Terminal, leveraging the fact that `say`, run on a short, repeated syllable spoken very quickly, can approximate a pitch.  For example,
```
say wuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwu --voice=Luciana --rate=720
```
approximates the pitch A3.  Given a melody, this app composes a combination of `say` commands that sings this melody.

## Getting Started

This app should work out of the box, on a computer with Mac Terminal and Python 2.7 installed.

## Usage

The main usage is
```
python play.py [in_file] [out_file]
```
This writes to `out_file` a `say` command that sings the melody from `in_file`.
For example:
```
python play.py sample_in/birthday2.txt sample_out/birthday2.txt
eval $(cat sample_out/birthday2.txt)
```
writes a `say` command for Happy Birthday to `sample_out/birthday2.txt` and executes this command.

### Changing the Pitch Map

The map from pitch to (syllable, voice) is stored in `config/pitch_map.config`.  Candidate (syllable, voice) combinations for each pitch are stored in `pitches.out`.

After changing the pitch map, run
```
python test_pitch.py
```
to regenerate auto-generated configs before running `play.py`.

## License

This project is licensed under the MIT License.

## Acknowledgments

Thanks to Next 4W and the MIT Undergrad Math Lounge for putting up with my obnoxious sound experimentation :)
