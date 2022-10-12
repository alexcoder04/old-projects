from ..config import config
from uuid import uuid4
from datetime import datetime
import os
import shutil
import json

class Cache:
    def __init__(self):
        self.CACHE_DIR = config.get("TEMP_PATH")
        self._file = os.path.join(self.CACHE_DIR, "cache.json")
        self.DEFAULT_CACHE_TIME = 60 * 5
        if not os.path.exists(self._file):
            f = open(self._file, "w")
            f.write("{}")
            f.close()
        self._cache = self._load()
    
    def set_cache(self, key, value, seconds=None):
        self._refresh()
        if not seconds: seconds = self.DEFAULT_CACHE_TIME
        self._cache[key] = [value, datetime.now().timestamp() + seconds]
        self._dump()
    
    def get_cache(self, key):
        self._refresh()
        try:
            [value, expires] = self._cache[key]
        except KeyError:
            return None
        else:
            if expires < datetime.now().timestamp():
                del self._cache[key]
                self._dump()
                return None
            return value
    
    def cache_file(self, path, seconds=None):
        self._refresh()
        if not seconds: seconds = self.DEFAULT_CACHE_TIME
        id = str(uuid4())
        shutil.copy(path, os.path.join(self.CACHE_DIR, "cache-" + id))
        self.set_cache("f-" + path, id, seconds)
    
    def get_cached_file(self, path, mode="r"):
        id = self.get_cache("f-" + path)
        if not id: return None
        try:
            with open(os.path.join(self.CACHE_DIR, id), mode) as f:
                return f.read()
        except FileNotFoundError:
            return None

    def _refresh(self):
        self._cache = self._load()

    def _load(self):
        return json.load(open(self._file, "r"))
    
    def _dump(self):
        json.dump(self._cache, open(self._file, "w"))

magnan_cache = Cache()
