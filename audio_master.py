import os.path
import subprocess

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
    for voice in VOICES:
        print voice
        if not os.path.isfile(OUT_DIR + voice + '.out'): # if an outfile doesn't exist for this voice
        	subprocess.call(['python', 'audio.py', voice])
    subprocess.call(['python', 'pitchify.py'])
