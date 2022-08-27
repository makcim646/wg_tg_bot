import subprocess
import os
import time
from db import log

       
def check_folders():
    if os.path.exists('png') != True:
        os.mkdir('png')
    if os.path.exists('conf') != True:
        os.mkdir('conf')
    text = f'{time.ctime()} path /png is {os.path.exists("png")}, path /conf is {os.path.exists("conf")} \n'
    log(text)
    

if __name__ == '__main__':
    check_folders()
    proc = subprocess.Popen('python3 bot.py', shell=True)
    
