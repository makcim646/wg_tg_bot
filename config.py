<<<<<<< Updated upstream
import configparser
import os


def create_config(path='setting.ini', bot_token='', admin_id=''):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("setting")
    config.set("setting", "bot_token", f'{bot_token}')
    config.set("setting", "admin_id", f'{admin_id}')

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path='setting.ini'):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    out = {}
    for key in config['setting']:
        out[key] = config['setting'][key]

    return out


def update_config(kwarg, path='setting.ini'):
    config = configparser.ConfigParser()
    config.read(path)
    for key in kwarg.keys():
        config.set('setting', key, kwarg[key])

    with open(path, "w") as config_file:
        config.write(config_file)
=======
import configparser
import os


def create_config(path='setting.ini', bot_token='', admin_id=''):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("setting")
    config.set("setting", "bot_token", f'{bot_token}')
    config.set("setting", "admin_id", f'{admin_id}')

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path='setting.ini'):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        bot_token = str(input('Input telegram bot token: '))
        admin_id = str(input('Input telegram id admin'))
        create_config(path, bot_token, admin_id)

    config = configparser.ConfigParser()
    config.read(path)
    out = {}
    for key in config['setting']:
        out[key] = config['setting'][key]

    return out


def update_config(kwarg, path='setting.ini'):
    config = configparser.ConfigParser()
    config.read(path)
    for key in kwarg.keys():
        config.set('setting', key, kwarg[key])

    with open(path, "w") as config_file:
        config.write(config_file)
>>>>>>> Stashed changes
        return True