from .storage import Storage
from .files import *
from .utils import init_temp
import os

init_temp()
storage = Storage()

def create_storage():
    from .views import app
    return app
