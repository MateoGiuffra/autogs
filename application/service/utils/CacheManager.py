import logging
import time 

class CacheManager:
    def __init__(self, timeout):
        self.timeout = timeout
        self.cache = {"summary": 0, "timestamp": 0, "message": None, "last_summary": 0}

    def get_cached_data(self):
        current_time = time.time()
        if self.cache["summary"] and current_time - self.cache["timestamp"] < self.timeout:
            return self.cache
        return None
    
    def get_last_summary(self):
        return self.cache["last_summary"]
    
    def get_summary(self):
        return self.cache["summary"]
    
    def update_cache(self, data):
        if self.cache["message"] is None:
             self.cache["message"] = f"El total actual es: {data}." 
             self.cache["last_summary"] = data
        last_total = self.cache["last_summary"]
        self.cache["last_summary"] = self.cache["summary"]
        self.cache["summary"] = data
        self.cache["timestamp"] = time.time()
        self.cache["message"] = f"El total actual es: {data}. Se obtuvieron {data - last_total} pesos más que la anterior vez."
    
    def last_month_summary_first_time(self):
        return self.cache["last_month_summary"] == 0
    
    def update_last_month(self, last_month_summary):
        self.cache["last_month_summary"] = last_month_summary