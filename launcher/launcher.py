# There is no way in heck the real launcher is gonna use Python. I'd kill for my JavaScript, I'd die for my TypeScript.

from shutil import copy
from os.path import abspath, dirname
import requests, os, subprocess, time

def main():
    print('Please enter your username below.')
    uName = input()
    res = requests.post('http://localhost:5000/launcher', data = {'username': uName})
    resJSON = res.json()
    # We will copy the file because it's hosted locally. Normally, this would download a file.
    clientJAR = os.path.join(dirname(abspath(__file__)), 'client.jar')
    copy(resJSON['download'], clientJAR)
    subprocess.call(['java', '-jar', clientJAR, str(resJSON['id'])], shell=True)
    time.sleep(2)
    os.remove(clientJAR)

if __name__ == "__main__":
    main()