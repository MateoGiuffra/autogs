import os

# Obtengo la ruta absoluta del directorio actual (donde está el script)
project_dir = os.path.dirname(os.path.abspath(__file__))

# Creo la carpeta Output si no existe
output_dir = os.path.join(project_dir, "Output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Creo la carpeta drivers si no existe
drivers_dir = os.path.join(project_dir, "drivers")
if not os.path.exists(drivers_dir):
    os.makedirs(drivers_dir)

# Ruta completa al archivo chromedriver.exe (o chromedriver en Linux/macOS)
chrome_driver_path = os.path.join(drivers_dir, "chromedriver.exe")  # Para Windows
# chrome_driver_path = os.path.join(drivers_dir, "chromedriver")  # Para Linux/macOS

# Verifico si el archivo chromedriver existe
if not os.path.exists(chrome_driver_path):
    raise FileNotFoundError(f"El archivo {chrome_driver_path} no existe. Por favor, coloca el ChromeDriver en la carpeta 'drivers'.")

# Asigno la ruta de salida a la variable dir
dir = output_dir

# Imprimo las rutas para verificar
print(f"Ruta del proyecto: {project_dir}")
print(f"Ruta de salida (Output): {output_dir}")
print(f"Ruta del ChromeDriver: {chrome_driver_path}")