import os 

class AbsPath:
     
     @staticmethod
     def obtener_abspath():
        # Obtengo la ruta absoluta del directorio actual (donde está el script)
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # Le agrego al path Output
        output_dir = os.path.join(project_dir,"Output")

        # Creo la carpeta si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        return output_dir
     