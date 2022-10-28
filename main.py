import subprocess
import json
import os
import time
from db import *


def check_folders():
    if not os.path.exists('png'):
        os.mkdir('png')

    if not os.path.exists('conf'):
        os.mkdir('conf')

    if not os.path.exists(f'db.json'):
        with open(f'db.json', 'w') as file:
            json.dump({}, file)

    if not os.path.exists(f'gift.json'):
        with open(f'gift.json', 'w') as file:
            json.dump({}, file)

    text = f'{time.ctime()} path /png is {os.path.exists("png")}, path /conf is {os.path.exists("conf")} \n'
    log(text)

def check_config():
    from config import get_config, update_config

    conf = get_config()
    admin = conf['admin_id']
    token = conf['bot_token']

    if admin == '':
        data = input('Input admin id: ')
        update_config({'admin_id':data})

    if token == '':
        data = input('Input telegram token: ')
        update_config({'bot_token':data})


def monitor_gift():
    oneday = 86400
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)


    for user in basa_users.keys():
        if basa_users[user]['gift']:
            print(time.time() - basa_users[user]['time'])
            if time.time() - basa_users[user]['time'] > 2500:
                close_gift(id_user)
                pass



if __name__ == '__main__':
    check_config()
    check_folders()
    proc = subprocess.Popen('python3 bot.py', shell=True)

    while True:
        monitor_gift()
        time.sleep(30)

