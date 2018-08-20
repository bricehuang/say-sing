import os.path
import subprocess
import sys

OUT_DIR = './outfiles/'
VOICES = [
    "Alex",
    "Alice",
    "Alva",
    "Amelie",
    "Anna",
    "Carmit",
    "Damayanti",
    "Daniel",
    "Diego",
    "Ellen",
    "Fiona",
    "Fred",
    "Ioana",
    "Joana",
    "Jorge",
    "Juan",
    "Kanya",
    "Karen",
    "Kyoko",
    "Laura",
    "Lekha",
    "Luca",
    "Luciana",
    "Maged",
    "Mariska",
    "Mei-Jia",
    "Melina",
    "Milena",
    "Moira",
    "Monica",
    "Nora",
    "Paulina",
    "Samantha",
    "Sara",
    "Satu",
    "Sin-ji",
    "Tessa",
    "Thomas",
    "Ting-Ting",
    "Veena",
    "Victoria",
    "Xander",
    "Yelda",
    "Yuna",
    "Yuri",
    "Zosia",
    "Zuzana",
]

if __name__ == '__main__':
    force = len(sys.argv) > 1 and (sys.argv[1]=='--force')
    for voice in VOICES:
        print voice
        # if an outfile doesn't exist for this voice, or force option being used
        if not os.path.isfile(OUT_DIR + voice + '.out') or force:
            subprocess.call(['python', 'generate_voice_data.py', voice])
    subprocess.call(['python', 'consolidate_voice_data.py'])
