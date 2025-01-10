from application.controller.APIREST.SummaryApi import SummaryApi
import psutil
import os 
# Instanciar la aplicación
app_routes = SummaryApi()
app = app_routes.app  


# Monitoreo de memoria
process = psutil.Process(os.getpid())
print(f"Memory usage after SummaryApi instantiation: {process.memory_info().rss / 1024 ** 2} MB")