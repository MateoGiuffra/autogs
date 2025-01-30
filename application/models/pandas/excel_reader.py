import pandas as pd
import locale 
def reader_get_total(path):
    try:
        locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')
        # leo el archivo (es un .xls pero es mentira, es un HTML)
        html_tables = pd.read_html(path, decimal=',', thousands='.', flavor='lxml') # esto devuelve una "lista" de data frames

        # por eso aca selecciono a la primer (y unica) tabla (data frame) de la lista 
        df = html_tables[0]

        # selecciono la columna del indice 15 (seria la P)
        column = df.iloc[:, 15]  

        #obtengo el ultimo valor de la columna
        last_value = column.iloc[-1]  
        return last_value

    except Exception as e:
        print("Error al leer el archivo: ", e)
        
    
    



