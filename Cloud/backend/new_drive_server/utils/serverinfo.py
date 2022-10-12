import subprocess
from ..config import config
import os

magnan_version = "0.0.2"

def get_server_ip():
    if os.getenv("MAGNAN_PROD") != "true":
        return "127.0.0.1"
    with subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE) as proc:
        raw_out = proc.stdout.read()
    ip = str(raw_out, encoding="utf8").split()[0]
    return ip

def get_port():
    print("WARNING! get_port() will be deprecated soon! Use config.get('PORT') instead!")
    return config.get("PORT")
