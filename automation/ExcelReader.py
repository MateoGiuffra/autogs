import pandas as pd
from io import StringIO

class ExcelReader:
    def __init__(self, path):
        self.path = path

    def get_total(self):
        # Leer todas las tablas HTML en el archivo
        df_list = pd.read_html(self.path)

        # Supongamos que la tabla que necesitas es la primera en la lista
        df = df_list[0]

        # Convertir la tabla a un archivo Excel (.xlsx)
        df.to_excel('archivo_convertido.xlsx', index=False)

        # Ahora puedes trabajar con el archivo Excel convertido
        df_excel = pd.read_excel('archivo_convertido.xlsx')

        # Filtrar la columna 'P' y eliminar los valores nulos
        columna_p = df_excel['P'].dropna()

        # Obtener el último valor no nulo de la columna 'P'
        ultimo_valor = columna_p.iloc[-1]

        print(ultimo_valor)

    # def get_total(self):
    #     try:
    #         # Intentar leer el archivo sin especificar la codificación o con una alternativa
    #         with open(self.path, "r", encoding="ISO-8859-1") as file:
    #             html_content = file.read()

    #         # Usar StringIO para evitar el FutureWarning
    #         html_io = StringIO(html_content)

    #         # Leer las tablas del contenido HTML
    #         df_list = pd.read_html(html_io)
    #         df = df_list[0]  # Extraer la primera tabla del HTML

    #         # Verificar las columnas disponibles en el DataFrame
    #         print("Columnas disponibles:", df.columns)

    #         # Buscar la fila que contiene "Totales"
    #         for index, row in df.iterrows():
    #             if "Totales" in row.to_string():
    #                 # Filtrar solo los valores numéricos (eliminando celdas vacías)
    #                 row_values = row.dropna()  # Eliminar valores nulos (celdas vacías)

    #                 # Obtener el anteúltimo valor
    #                 if len(row_values) > 1:  # Asegurarse de que hay al menos 2 valores
    #                     anteultimo_valor = row_values.iloc[-2]  # Obtener el anteúltimo valor
    #                     print(f"Anteúltimo valor encontrado: {anteultimo_valor}")
    #                     return anteultimo_valor
    #                 else:
    #                     print("No hay suficientes valores en la fila 'Totales'.")
    #                     return None

    #     except Exception as e:
    #         print(f"Error al leer el archivo HTML: {e}")
    #         return None
