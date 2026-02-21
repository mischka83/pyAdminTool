import json
from pathlib import Path
from cryptography.fernet import Fernet
import os

CONFIG_FILE = Path(__file__).parent.parent / "config.json"
KEY_FILE = Path(__file__).parent.parent / "secret.key"

# Schlüssel laden
def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

fernet = Fernet(load_key())

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            # Passwort entschlüsseln
            if config.get("password"):
                config["password"] = fernet.decrypt(config["password"].encode()).decode()
            return config
    return {
        "ldaps_url": "",
        "username": "",
        "password": "",
        "feld4": "",
        "feld5": ""
    }

def save_config(config):
    # Passwort verschlüsseln
    encrypted_password = fernet.encrypt(config["password"].encode()).decode()
    config_to_save = config.copy()
    config_to_save["password"] = encrypted_password
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_to_save, f, indent=4)