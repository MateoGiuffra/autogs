import pandas as pd
import locale 

class ExcelReader:
    def __init__(self, path):
        self.path = path
        # Se configura el locale para que reconozca la coma como decimal
        locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')

    def get_total(self):
        try:
            # leo el archivo (es un .xls pero es mentira, es un HTML)
            html_tables = pd.read_html(self.path, decimal=',', thousands='.') # esto devuelve una "lista" de data frames

            # por eso aca selecciono a la primer (y unica) tabla (data frame) de la lista 
            df = html_tables[0]

            # selecciono la columna del indice 15 (seria la P)
            column = df.iloc[:, 15]  

            #obtengo el ultimo valor de la columna
            last_value = column.iloc[-1]  
            return last_value
    
        except Exception as e:
            print("Error al leer el archivo: ", e)
        
    
    



