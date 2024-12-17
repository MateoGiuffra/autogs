# import unittest
# from unittest.mock import patch
# import pandas as pd
# from automation.ExcelReader import ExcelReader 
# from io import StringIO

# class TestExcelReader(unittest.TestCase):
    
#     @patch('pandas.read_excel')  # Mockear la función read_excel
#     def test_get_total(self, mock_read_excel):
#         # Simular datos de un archivo Excel como un DataFrame
#         data = {
#             'P': [10, None, 20, 30, None]  # Columna P con valores y algunos nulos
#         }
#         df_mock = pd.DataFrame(data)
        
#         # Configurar el mock para que pandas.read_excel devuelva nuestro DataFrame falso
#         mock_read_excel.return_value = df_mock
        
#         # Crear una instancia de ExcelReader
#         reader = ExcelReader('archivo_falso.xlsx')
        
#         # Ejecutar el método get_total
#         resultado = reader.get_total()
        
#         # Verificar que el resultado sea correcto (último valor no nulo de la columna P: 30)
#         self.assertEqual(resultado, 30)

# if __name__ == '__main__':
#     unittest.main()
