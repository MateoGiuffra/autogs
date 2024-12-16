from decouple import config  
import os 
from automation.WebDriverManager import WebDriverManager

def main():

    url = "https://game.systemmaster.com.ar/frmLogin.aspx"
    user = config("DB_USER")
    password = config("DB_PASSWORD")

    output_path = obtener_abspath()
    expected_filename_pattern = 'rptCobranzas*.xls'

    web_driver_manager = WebDriverManager(output_path, expected_filename_pattern)
    web_driver_manager.start(url, user, password)


def obtener_abspath():
    # Obtengo la ruta absoluta del directorio actual (donde está el script)
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Le agrego al path Output
    output_dir = os.path.join(project_dir, "Output")

    # Creo la carpeta si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    return output_dir

if __name__ == "__main__":
    main()