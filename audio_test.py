import subprocess
import sys

DEFAULT_REPEATS = 100
if __name__ == '__main__':
	sound = sys.argv[1]
	voice = sys.argv[2]
	repeats = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_REPEATS
	subprocess.call(['say', sound*repeats, '--voice='+voice, '--rate=720'])
