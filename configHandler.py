import os
import configparser
from dexShareCredentials import DexShareCredentials

def create_config_file():
    credentials_window = DexShareCredentials()
    credentials_window.present()

def load_credentials():
    config_exists = os.path.isfile('config.ini')
    if config_exists:
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'Credentials' in config:
          username = config['Credentials'].get('Username', '')
          password = config['Credentials'].get('Password', '')
          ous = config['Credentials'].get('ous', '')
          print(f"Loaded credentials for {username}")
          return username, password, ous
        if username and password:
          credentials_window.username_entry.set_text(username)
          credentials_window.password_entry.set_text(password)
        if ous == 'True':
          credentials_window.ous_check.set_active(True)
        else:
          credentials_window.ous_check.set_active(False)

    return None, None, None

def save_credentials(username, password, ous):
    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'Credentials' not in config:
        config['Credentials'] = {}

    config['Credentials']['Username'] = username
    config['Credentials']['Password'] = password
    config['Credentials']['ous'] = ous

    with open('config.ini', 'w') as configfile:
        config.write(configfile)