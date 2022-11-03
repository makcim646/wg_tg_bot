<<<<<<< Updated upstream
import subprocess
import json
import time


def creat_new_user(id_user):
    #добовляет нового пользователя в свою базу и создает для него конфиг в wireguard
    id_user = str(id_user)
    if subprocess.call(["./newclient.sh", id_user]) == 0:
        add_in_db(id_user)
        return 'creat'
    else:
        return 'error'


def root_add(id_user):
    #создает навовый конфиг для подключения к wireguard
    id_user = str(id_user)
    if subprocess.call(["./newclient.sh", id_user]) == 0:
        add_in_db(id_user)
        return 'creat'
    else:
        return 'error'


def client_list():
    with open('db.json', 'r') as file:
        basa_users = json.load(file)

    return [user for user in basa_users.keys()]

def gift_list():
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)

    return [user for user in basa_users.keys()]


def check_in_db(id_user):
    #Проверяет есть ли пользователь в базе и есть ли у него действующий активный конфиг если есть вернет true, если нету false
    id_user = str(id_user)
    with open('db.json', 'r') as file:
        basa_users = json.load(file)

    if basa_users.get(id_user) == None:
        return False

    if basa_users[id_user]['status'] == 'active':
        return True

    return False


def add_in_db(id_user):
    #добовление пользователя в свою базу данных
    id_user = str(id_user)
    with open('db.json', 'r') as file:
        basa_users = json.load(file)


    if basa_users.get(id_user) == None:
        basa_users[id_user] = {'time': time.time(), 'status': 'active', 'day': 31}
    else:
        basa_users[id_user]['status'] = 'active'
        basa_users[id_user]['time'] = time.time()
        basa_users[id_user]['day'] = 31

    #print(basa_users.get(id_user))

    with open('db.json', 'w') as file_in:
        json.dump(basa_users, file_in, indent=4)


def add_gift_db(id_user):
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)

    id_user = str(id_user)
    if basa_users.get(id_user) == None:
        basa_users[id_user] = {'time': time.time(), 'gift':True}


    with open('gift.json', 'w') as file_in:
        json.dump(basa_users, file_in, indent=4)


def gift(id_user):
    #добовляет нового пользователя в свою базу и создает для него конфиг в wireguard
    id_user = str(id_user)
    if subprocess.call(["./newclient.sh", id_user]) == 0:
        add_gift_db(id_user)
        return True
    else:
        return False


def check_gift(id_user):
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)

    id_user = str(id_user)

    if basa_users.get(id_user) == None:
        return True
    else:
        return False


def close_gift(id_user):
    id_user = str(id_user)
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)

    if subprocess.call(["./revokeclient.sh", id_user]) == 0:
        basa_users[id_user]['gift'] = False

        with open('gift.json', 'w') as file_in:
            json.dump(basa_users, file_in, indent=4)
            return True




def deactive_user_db(id_user):
    #удаеть конфиг клиента из wireguard и отмечает это в своей базе
    id_user = str(id_user)
    with open('db.json', 'r') as file:
        basa_users = json.load(file)


    if basa_users.get(id_user) == None:
        return False

    if subprocess.call(["./revokeclient.sh", id_user]) == 0:
        basa_users[id_user]['status'] = 'deactive'
        basa_users[id_user]['day'] = 0

        with open('db.json', 'w') as file_in:
            json.dump(basa_users, file_in, indent=4)
        return True


def log(text):
    with open('log', 'a') as file:
        file.writelines(str(text))



if __name__ == "__main__":
    #add_in_db(34342322)
    pass





=======
import subprocess
import json
import time


def creat_new_user(id_user):
    #добовляет нового пользователя в свою базу и создает для него конфиг в wireguard
    id_user = str(id_user)
    if subprocess.call(["./newclient.sh", id_user]) == 0:
        add_in_db(id_user)
        return 'creat'
    else:
        return 'error'


def root_add(id_user):
    #создает навовый конфиг для подключения к wireguard
    id_user = str(id_user)
    if subprocess.call(["./newclient.sh", id_user]) == 0:
        add_in_db(id_user)
        return 'creat'
    else:
        return 'error'


def client_list():
    with open('db.json', 'r') as file:
        basa_users = json.load(file)

    return [user for user in basa_users.keys()]

def gift_list():
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)

    return [user for user in basa_users.keys()]


def check_in_db(id_user):
    #Проверяет есть ли пользователь в базе и есть ли у него действующий активный конфиг если есть вернет true, если нету false
    id_user = str(id_user)
    with open('db.json', 'r') as file:
        basa_users = json.load(file)

    if basa_users.get(id_user) == None:
        return False

    if basa_users[id_user]['status'] == 'active':
        return True

    return False


def add_in_db(id_user):
    #добовление пользователя в свою базу данных
    id_user = str(id_user)
    with open('db.json', 'r') as file:
        basa_users = json.load(file)


    if basa_users.get(id_user) == None:
        basa_users[id_user] = {'time': time.time(), 'status': 'active', 'day': 31}
    else:
        basa_users[id_user]['status'] = 'active'
        basa_users[id_user]['time'] = time.time()
        basa_users[id_user]['day'] = 31

    #print(basa_users.get(id_user))

    with open('db.json', 'w') as file_in:
        json.dump(basa_users, file_in, indent=4)


def add_gift_db(id_user):
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)

    id_user = str(id_user)
    if basa_users.get(id_user) == None:
        basa_users[id_user] = {'time': time.time(), 'gift':True}


    with open('gift.json', 'w') as file_in:
        json.dump(basa_users, file_in, indent=4)


def gift(id_user):
    #добовляет нового пользователя в свою базу и создает для него конфиг в wireguard
    id_user = str(id_user)
    if subprocess.call(["./newclient.sh", id_user]) == 0:
        add_gift_db(id_user)
        return True
    else:
        return False


def check_gift(id_user):
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)

    id_user = str(id_user)

    if basa_users.get(id_user) == None:
        return True
    else:
        return False


def close_gift(id_user):
    id_user = str(id_user)
    with open('gift.json', 'r') as file:
        basa_users = json.load(file)

    if subprocess.call(["./revokeclient.sh", id_user]) == 0:
        basa_users[id_user]['gift'] = False

        with open('gift.json', 'w') as file_in:
            json.dump(basa_users, file_in, indent=4)
            return True




def deactive_user_db(id_user):
    #удаеть конфиг клиента из wireguard и отмечает это в своей базе
    id_user = str(id_user)
    with open('db.json', 'r') as file:
        basa_users = json.load(file)


    if basa_users.get(id_user) == None:
        return False

    if subprocess.call(["./revokeclient.sh", id_user]) == 0:
        basa_users[id_user]['status'] = 'deactive'
        basa_users[id_user]['day'] = 0

        with open('db.json', 'w') as file_in:
            json.dump(basa_users, file_in, indent=4)
        return True


def log(text):
    with open('log', 'a') as file:
        file.writelines(str(text))



if __name__ == "__main__":
    #add_in_db(34342322)
    pass





>>>>>>> Stashed changes
