import logging
import time 

class CacheManager:
    def __init__(self, timeout):
        self.timeout = timeout
        self.cache = {"summary": None, "timestamp": 0}

    def get_cached_data(self):
        current_time = time.time()
        if self.cache["summary"] and current_time - self.cache["timestamp"] < self.timeout:
            return self.cache["summary"]
        return None

    def update_cache(self, data):
        self.cache["summary"] = data
        self.cache["timestamp"] = time.time()