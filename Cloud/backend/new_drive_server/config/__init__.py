import json

CONFIG_FILE = "/etc/magnan/magnan.conf"

class Config:
    _default = {
        "PORT": 5000,
        "USER_FILES_PATH": "/var/magnan_storage/user",
        "TEMP_PATH": "/tmp/magnan",
        "IMAGE_COMPRESSED_RESOLUTION": (50, 50),
        "STATIC_SERVER_PORT": 8000,
        "MUSIC_FOLDER": "/var/magnan/musik",
        "MAX_CONTENT_LENGTH": 1024 * 1024 * 50,
        "ACTIVATED_PLUGINS": [],
        "PLUGINS_DIR": "/var/magnan/plugins",
        "LOGS_DIR": "/var/magnan/logs"
    }

    def __init__(self):
        try:
            self._conf_dict = json.load(open(CONFIG_FILE))
        except FileNotFoundError:
            self._conf_dict = self._default
    
    def get(self, key):
        try:
            return self._conf_dict[key]
        except KeyError:
            return None

config = Config()
