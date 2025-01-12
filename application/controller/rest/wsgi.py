from application.controller.rest.SummaryREST import SummaryREST
import psutil
import os 
# Instanciar la aplicación
app_routes = SummaryREST()
app = app_routes.app  


# Monitoreo de memoria
process = psutil.Process(os.getpid())
print(f"Memory usage after SummaryApi instantiation: {process.memory_info().rss / 1024 ** 2} MB")